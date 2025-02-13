from typing import Annotated, Any, Callable, Optional
import pandas as pd
from functools import wraps

from .basics import Audience, Datasource
from .utils import AggFunctionName, convert_series_unit, safe_copy
from ..client.pvradar_resources import PvradarResourceType, unit_for_pvradar_resource_type
from ..common.pandas_utils import SeriesOrFrame, is_series_or_frame


def _apply_attr(data: Optional[SeriesOrFrame], attr_name: str, attr_value: Any) -> Optional[SeriesOrFrame]:
    if data is None:
        return None
    if not isinstance(data, (pd.Series, pd.DataFrame)):
        raise ValueError(f'Expected pd.Series or pd.DataFrame while applying {attr_name}, got: {type(data)}')
    current_attr = data.attrs.get(attr_name)
    if current_attr == attr_value:
        return data

    new_data = safe_copy(data)
    new_data.attrs[attr_name] = attr_value
    return new_data


def _apply_consistent_attr(data: Optional[SeriesOrFrame], attr_name: str, attr_value: Any) -> Optional[SeriesOrFrame]:
    if data is None:
        return
    if not isinstance(data, (pd.Series, pd.DataFrame)):
        raise ValueError(
            f'Expected pd.Series or pd.DataFrame while applying {attr_name}, got: {type(data)}. '
            + 'Did you forget scalar=True?'
        )
    current_attr = data.attrs.get(attr_name)

    if current_attr is not None and current_attr != attr_value:
        raise ValueError(
            f'Conflicting attributes, trying to set {attr_name}="{attr_value}" but already set to "{current_attr}"'
        )

    if current_attr == attr_value:
        return data

    new_data = safe_copy(data)
    new_data.attrs[attr_name] = attr_value
    return new_data


def label(label: str):
    def decorator(func):
        func.label = label

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result = _apply_attr(result, 'label', label)
            return result

        return wrapper

    return decorator


def name(name: str):
    def decorator(func):
        func.__name__ = name
        return func

    return decorator


def resource_type(
    resource_type_param: str,
    *,
    rename: Annotated[str | bool | None, 'rename series or use resource_type as name'] = None,
    validate: Annotated[bool, 'ensure that another resource_type is not overwritten'] = False,
    scalar: Annotated[bool, 'result will have no metadata, resource_type will only be used for binding'] = False,
):
    def decorator(func):
        func.resource_type = resource_type_param

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if not scalar:
                if validate:
                    result = _apply_consistent_attr(result, 'resource_type', resource_type_param)
                else:
                    result = _apply_attr(result, 'resource_type', resource_type_param)

                if rename:
                    if not isinstance(result, pd.Series):
                        raise ValueError(f'rename is only supported for pd.Series values, got: {type(result)}')
                    new_name = result.name if isinstance(rename, str) else resource_type_param
                    if result.name != new_name:
                        result = result.copy()
                        result.name = new_name

            return result

        return wrapper

    return decorator


def pvradar_resource_type(
    resource_type_param: PvradarResourceType,
    *,
    use_std_unit: Annotated[bool, 'Convert to std PVRADAR units for given resource type'] = False,
    rename: Annotated[str | bool | None, 'rename series or use resource_type as name'] = None,
    validate: Annotated[bool, 'ensure that another resource_type is not overwritten'] = False,
):
    if use_std_unit:
        unit = unit_for_pvradar_resource_type(resource_type_param)
        if not unit:
            raise ValueError(f'No standard unit for {resource_type_param}')

        def decorator(func):
            func.resource_type = resource_type_param
            func.unit = unit

            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if validate:
                    result = _apply_consistent_attr(result, 'resource_type', resource_type_param)
                else:
                    result = _apply_attr(result, 'resource_type', resource_type_param)

                if not isinstance(result, pd.Series):
                    raise ValueError(f'use_std_unit is only supported for pd.Series values, got: {type(result)}')
                result = convert_series_unit(result, to_unit=unit)  # type: ignore

                if isinstance(rename, str):
                    result.name = rename
                elif rename:
                    result.name = resource_type_param

                return result

            return wrapper

        return decorator
    else:
        return resource_type(str(resource_type_param), rename=rename)


def datasource(datasource: Datasource):
    def decorator(func):
        func.datasource = datasource

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result = _apply_consistent_attr(result, 'datasource', datasource)
            return result

        return wrapper

    return decorator


def to_unit(unit: str):
    def decorator(func):
        func.unit = unit

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.Series):
                if 'unit' in result.attrs:
                    return convert_series_unit(result, from_unit=result.attrs['unit'], to_unit=unit)
                else:
                    raise ValueError('No unit provided to convert from. Use set_unit decorator instead')
            else:
                raise ValueError(f'to_unit is only supported for pd.Series values, got: {type(result)}')

        return wrapper

    return decorator


def set_unit(unit: str):
    def decorator(func):
        func.unit = unit

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result = _apply_attr(result, 'unit', unit)
            return result

        return wrapper

    return decorator


def update_attrs(
    *,
    datasource: Optional[Datasource] = None,
    unit: Optional[str] = None,
    agg: Optional[AggFunctionName] = None,
    freq: Optional[str] = None,
    **kwargs,
):
    def decorator(func):
        if datasource is not None:
            func.datasource = datasource

        if unit is not None:
            func.unit = unit

        @wraps(func)
        def wrapper(*args, **nested_kwargs):
            result = func(*args, **nested_kwargs)

            if result is None:
                return None
            if not is_series_or_frame(result):
                raise ValueError(f'Expected pd.Series or pd.DataFrame while updating attrs, got: {type(result)}')

            attr_patch = kwargs

            # TODO: add validation of well-known attrs
            if datasource is not None:
                attr_patch['datasource'] = datasource
            if unit is not None:
                attr_patch['unit'] = unit
            if agg is not None:
                attr_patch['agg'] = agg
            if freq is not None:
                attr_patch['freq'] = freq

            result = safe_copy(result)
            result.attrs.update(attr_patch)  # type: ignore
            return result

        return wrapper

    return decorator


def cache_key(cache_key: str | Callable):
    def decorator(func):
        func.cache_key = cache_key
        return func

    return decorator


def series_name(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.Series):
                result.name = name
            else:
                raise ValueError(f'series_name is only supported for pd.Series values, got: {type(result)}')
            return result

        return wrapper

    return decorator


def audience(org_ids: list[str] | str = [], project_goals: list[str] | str = []):
    def decorator(func):
        nonlocal org_ids, project_goals
        if isinstance(org_ids, str):
            org_ids = [org_ids]
        any_org = '*' in org_ids
        if isinstance(project_goals, str):
            project_goals = [project_goals]
        func.audience = Audience(any_org=any_org, org_ids=org_ids, project_goals=project_goals)
        return func

    return decorator
