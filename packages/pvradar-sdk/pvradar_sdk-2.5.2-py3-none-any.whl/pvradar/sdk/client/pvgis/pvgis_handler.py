from ...modeling.model_context import ModelContext
from ...modeling.library_manager import BaseLibraryHandler, extract_models
from . import pvgis_models


class PvgisLibraryHandler(BaseLibraryHandler):
    def get_models(self):
        models = extract_models(pvgis_models)
        return models

    def enrich_context(self, context: ModelContext) -> None:
        super().enrich_context(context)
        context.register_model(pvgis_models.pvgis_seriescalc_table, for_resource_type=True)
        context.register_model(pvgis_models.pvgis_global_horizontal_irradiance, for_resource_type=True)


pvgis_handler = PvgisLibraryHandler()
