import json
from pathlib import Path
from typing import Any, Optional

import pandas as pd

from ..common.pandas_utils import crop_by_interval, is_series_or_frame
from ..data_case.deserializer import data_case_to_any
from ..data_case.serializer import any_to_data_case
from ..modeling.basics import BindingNotFound
from ..client.platform.pvradar_project import PvradarProject
from ..modeling.model_context import ModelContext
from ..modeling.model_binder import AbstractBinder, ModelParam
from ..modeling.model_wrapper import ModelBinding, ModelWrapper


def _read_from_file(
    file_caching_file_path: Path,
    interval: pd.Interval,
):
    with open(file_caching_file_path, 'r') as file:
        data_case = json.load(file)
    result = data_case_to_any(data_case)
    if is_series_or_frame(result):
        result = crop_by_interval(result, interval)
    return result


_read_from_file_wrapped = ModelWrapper(_read_from_file)


class FileCachingBinder(AbstractBinder):
    def __init__(self, path: Path | str):
        super().__init__()
        if isinstance(path, str):
            path = Path(path)
        self.path: Path = path
        self._file_map = None

    @property
    def file_map(self):
        if self._file_map is None:
            self._file_map = dict()
            for file in self.path.glob('*.json'):
                self._file_map[file.stem] = file
        return self._file_map

    def make_key(
        self,
        *,
        resource_name: str,
        as_param: Optional[ModelParam] = None,
        defaults: Optional[dict[str, Any]] = None,
        context: Optional[ModelContext] = None,
    ) -> str | None:
        if not context:
            return None
        project_id = context.get('project_id', '')
        if not project_id:
            raise ValueError('{self.__class__.__name__} requires project_id pre-defined in context')
        if resource_name == '_anonymous':
            if not as_param or not as_param.attrs:
                return None
            if 'resource_type' not in as_param.attrs:
                return None
            return project_id + '__' + as_param.attrs['resource_type']
        else:
            return project_id + '__' + resource_name

    def store_by_resource_type(self, context: PvradarProject, resource: Any):
        serialized = any_to_data_case(resource)
        resource_type = ''
        if isinstance(resource, pd.DataFrame) or isinstance(resource, pd.Series):
            resource_type = resource.attrs.get('resource_type', '')
        if not resource_type:
            raise ValueError('resource_type not found in resource')
        project_id = context.get('project_id', '')
        file = self.path / f'{project_id}__{resource_type}.json'
        file.write_text(json.dumps(serialized, indent=2))
        return file

    def bind(
        self,
        *,
        resource_name: str,
        as_param: Optional[ModelParam] = None,
        defaults: Optional[dict[str, Any]] = None,
        context: Optional[ModelContext] = None,
    ):
        key = self.make_key(resource_name=resource_name, as_param=as_param, defaults=defaults, context=context)
        if key in self.file_map:
            return ModelBinding(_read_from_file_wrapped, {'file_caching_file_path': self.file_map[key]})
        return BindingNotFound
