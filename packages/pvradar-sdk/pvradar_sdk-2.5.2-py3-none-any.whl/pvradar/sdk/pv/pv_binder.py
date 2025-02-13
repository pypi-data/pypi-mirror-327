from typing import Any, Optional

from ..modeling.geo_located_model_context import GeoLocatedModelContext
from ..modeling.basics import BindingNotFound, ModelParam
from ..modeling.model_context import ModelContext
from ..modeling.model_binder import AbstractBinder

_known_properties = [
    'array',
    'module',
    'structure',
]


class PvBinder(AbstractBinder):
    def bind(
        self,
        *,
        resource_name: str,
        as_param: Optional[ModelParam] = None,
        defaults: Optional[dict[str, Any]] = None,
        context: Optional[ModelContext] = None,
    ) -> Any:
        assert isinstance(context, GeoLocatedModelContext), (
            f'PvBinder requires a GeoLocatedModelContext, got {context.__class__.__name__}'
        )
        if resource_name in _known_properties:
            return getattr(context, resource_name)
        return BindingNotFound
