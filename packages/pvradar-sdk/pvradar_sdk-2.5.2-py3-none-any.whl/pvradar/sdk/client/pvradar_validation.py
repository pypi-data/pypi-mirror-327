from typing import Mapping, NotRequired
from pydantic import ConfigDict, TypeAdapter, ValidationError
from ..modeling.basics import Attrs


def validate_typed_dict(data: dict | Mapping, typed_dict_class: type) -> None:
    class AdjustedDict(typed_dict_class):
        __pydantic_config__ = ConfigDict(extra='forbid')

    ta = TypeAdapter(AdjustedDict)
    try:
        ta.validate_python(data)
    except ValidationError as e:
        f = e.errors()[0]
        raise ValueError(f'Validation failed for {typed_dict_class.__name__}: {f["type"]}, for {f["loc"]}: {f["msg"]}')


class NoExtrasAttrs(Attrs):
    resource_type: NotRequired[str]  # type: ignore
    __pydantic_config__ = ConfigDict(extra='forbid')  # type: ignore


ta_NoExtrasAttrs = TypeAdapter(NoExtrasAttrs)


def validate_pvradar_attrs(data: Mapping) -> None:
    try:
        ta_NoExtrasAttrs.validate_python(data)
    except ValidationError as e:
        f = e.errors()[0]
        raise ValueError(f'Bad PVRADAR Attrs: {f["msg"]} {f["loc"]} in {data}')
