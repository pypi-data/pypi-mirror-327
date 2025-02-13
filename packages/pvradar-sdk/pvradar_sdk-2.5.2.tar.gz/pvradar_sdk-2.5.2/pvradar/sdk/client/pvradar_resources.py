from typing import Any, NotRequired, Optional, TypeGuard, get_args
import pandas as pd
from pydantic import Field
from typing_extensions import Annotated as A

from ..modeling.basics import SeriesAttrs, PvradarResourceType


class SeriesConfigAttrs(SeriesAttrs):
    param_names: NotRequired[list[str]]


class PvradarSeriesConfigAttrs(SeriesConfigAttrs):
    resource_type: NotRequired[PvradarResourceType]  # type: ignore


S = PvradarSeriesConfigAttrs

_possible_pvradar_resource_types = get_args(PvradarResourceType.__value__)


def check_is_pvradar_resource_type(name: str) -> TypeGuard[PvradarResourceType]:
    return name in _possible_pvradar_resource_types


pvradar_resource_annotations: dict[PvradarResourceType, Any] = {
    'air_temperature': A[float, Field(ge=0), S(unit='degC')],
    'air_density': A[float, Field(ge=0), S(unit='kg/m^3')],
    'particle_mixing_ratio': A[pd.Series, Field(ge=0), S(unit='kg/kg', param_names=['particle_name'])],
    'particle_volume_concentration': A[
        pd.Series,
        Field(description='The mass of suspended particles in the air per unit volume'),
        S(param_names=['particle_name'], unit='kg/m^3'),
    ],
    'pm2_5_volume_concentration': A[
        pd.Series,
        Field(
            description='The total particulate matter concentration air'
            + ' including all contaminants with a diameter below 2.5 µm'
        ),
        S(param_names=['particle_name'], unit='kg/m^3'),
    ],
    'pm10_volume_concentration': A[
        pd.Series,
        Field(
            description='The total particulate matter concentration air'
            + ' including all contaminants with a diameter below 10 µm'
        ),
        S(param_names=['particle_name'], unit='kg/m^3'),
    ],
    'rainfall': A[pd.Series, Field(ge=0, description='The amount of rain (liquid water)'), S(unit='mm')],
    'rainfall_mass_rate': A[
        pd.Series,
        Field(ge=0, description='The mass of rain (liquid water) per area per time unit'),
        S(unit='kg/m^2/h'),
    ],
    'rainfall_rate': A[
        pd.Series,
        Field(ge=0, description='The amount of rainwater volume falling per unit area per unit time.'),
        S(unit='mm/h'),
    ],
    'relative_humidity': A[float, Field(ge=0), S(unit='%')],
    'snow_density': A[float, Field(ge=0, description='The mass of snow per volume unit'), S(unit='kg/m^3')],
    'snow_depth': A[float, Field(ge=0, description='The height of snow on the ground'), S(unit='mm')],
    'snow_depth_water_equivalent': A[
        float, Field(ge=0, description='The height of liquid water produced by melting all snow on the ground'), S(unit='mm')
    ],
    'snowfall': A[pd.Series, Field(ge=0, description='The height of snow accumulated over a period'), S(unit='mm')],
    'snowfall_water_equivalent': A[
        pd.Series,
        Field(ge=0, description='The height of liquid water produced by melting all snow that fell during a period'),
        S(unit='mm'),
    ],
    'snowfall_mass_rate': A[
        pd.Series,
        Field(ge=0, description='The mass of snow falling per area per time unit'),
        S(unit='kg/m^2/h'),
    ],
    'snowfall_rate': A[
        pd.Series,
        Field(ge=0, description='The amount of snow volume falling per unit area per unit time.'),
        S(unit='mm/h'),
    ],
    'soiling_level': A[pd.Series, Field(ge=0, le=1), S(unit='1')],
    'soiling_level_value': A[float, Field(ge=0, le=1), S(unit='1')],
    'soiling_rate': A[pd.Series, S(unit='1/h')],
    'soiling_ratio': A[pd.Series, S(unit='1')],
    'wind_speed': A[float, Field(ge=0), S(unit='m/s')],
}


def extract_unit_from_annotation(v: Any) -> Optional[str]:
    if isinstance(v, type(A[Any, Any])):  # type: ignore
        if hasattr(v, '__metadata__'):
            for maybe_attrs in v.__metadata__:  # type: ignore
                if isinstance(maybe_attrs, dict):
                    if 'unit' in maybe_attrs:
                        return maybe_attrs['unit']
                    if 'to_unit' in maybe_attrs:
                        return maybe_attrs['to_unit']
                    if 'set_unit' in maybe_attrs:
                        return maybe_attrs['set_unit']


def unit_for_pvradar_resource_type(resource_type: PvradarResourceType) -> Optional[str]:
    if resource_type not in pvradar_resource_annotations:
        raise ValueError(f'No standard pvradar annotation for {resource_type}')
    annotation = pvradar_resource_annotations[resource_type]
    unit = extract_unit_from_annotation(annotation)
    return unit
