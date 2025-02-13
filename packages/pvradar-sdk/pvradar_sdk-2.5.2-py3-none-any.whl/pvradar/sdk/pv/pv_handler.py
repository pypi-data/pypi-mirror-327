from ..modeling.model_binder import FirstMatchingTypeBinder
from ..modeling.library_manager import BaseLibraryHandler, extract_models
from . import pvlib_irradiance
from .pv_binder import PvBinder


class PvLibraryHandler(BaseLibraryHandler):
    def get_models(self):
        models = extract_models(pvlib_irradiance)
        return models

    def get_binders(self):
        return [
            PvBinder(),
            FirstMatchingTypeBinder(self.get_models(), name='pvlib_irradiance'),
        ]


pv_handler = PvLibraryHandler()
