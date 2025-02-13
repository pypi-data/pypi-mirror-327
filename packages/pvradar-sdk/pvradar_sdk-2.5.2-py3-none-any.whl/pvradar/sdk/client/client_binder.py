import inspect
from typing import Any, Mapping, Optional

from ..modeling.model_wrapper import ModelBinding
from ..modeling.model_context import ModelContext
from ..modeling.model_binder import AbstractBinder
from ..client.pvradar_resources import check_is_pvradar_resource_type
from ..modeling.basics import BaseResourceAttrs, BindingNotFound, ModelParam

from .models import standard_soiling_models
from .models import merra2_models
from .models import era5_models
from .models import noaa_models


pvradar_client_models = dict()


def _import_models(module_instance: Any):
    members = inspect.getmembers(module_instance)
    for name, obj in members:
        if inspect.isfunction(obj) and hasattr(obj, 'resource_type'):
            pvradar_client_models[name] = obj


_import_models(standard_soiling_models)
_import_models(merra2_models)
_import_models(era5_models)
_import_models(noaa_models)


class PvradarClientBinder(AbstractBinder):
    def __call__(self, *args, **kwargs):
        return self.bind(*args, **kwargs)

    def bind(
        self,
        *,
        resource_name: str,
        as_param: Optional[ModelParam] = None,
        defaults: Optional[dict[str, Any]] = None,
        context: Optional[ModelContext] = None,
    ) -> Any:
        name = resource_name
        defaults = defaults or {}

        attrs: Mapping = {}

        datasource: Optional[str] = None

        if as_param and as_param.attrs is not None:
            attrs = as_param.attrs
            if 'resource_type' in attrs:
                name = attrs['resource_type']
            if 'datasource' in attrs:
                datasource = attrs['datasource']

        candidate: ModelBinding | type[BindingNotFound] = BindingNotFound

        if not check_is_pvradar_resource_type(name):
            return BindingNotFound

        for obj in pvradar_client_models.values():
            if name in getattr(obj, 'resource_type'):
                extended_defaults = defaults.copy()
                base_attrs = BaseResourceAttrs.__optional_keys__
                for k in attrs:
                    if k not in base_attrs:
                        extended_defaults[k] = attrs[k]
                candidate = ModelBinding(model=obj, defaults=extended_defaults)

                if datasource:
                    if hasattr(obj, 'datasource') and datasource == obj.datasource:
                        return candidate
                else:
                    # short-circuit if datasource is not required, then first match is good enough
                    return candidate

        return BindingNotFound
