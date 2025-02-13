import inspect
from dataclasses import dataclass, field
from types import NoneType
from typing import Any, Literal, Mapping, NotRequired, Optional, Type, TypeGuard, TypedDict, get_args

Datasource = Literal[
    'merra2',
    'era5',
    'noaa',
    'pvgis',
]
AggFunctionName = Literal[
    'sum',
    'mean',
    'std',
    'min',
    'max',
    'count',
    'first',
    'last',
    'median',
]
DataType = Literal[
    'any',
    'float',
    'int',
    'string',
    'datetime',  # normally pd.Timestamp
    'unix_timestamp',
    'sweep_range',
    'table',
    'series',
]

type PvradarResourceType = Literal[
    # irradiance ----------------------------------------
    'solar_zenith_angle',
    'solar_azimuth_angle',
    'solar_elevation_angle',
    'plane_of_array_irradiance',
    'direct_normal_irradiance',
    'diffuse_horizontal_irradiance',
    'global_horizontal_irradiance',
    'angle_of_incidence',
    'surface_azimuth_angle',
    'surface_tilt_angle',
    'tracker_rotation_angle',
    #
    # meteo ---------------------------------------------
    'air_density',
    'air_temperature',
    'particle_mixing_ratio',
    'particle_volume_concentration',
    'pm10_volume_concentration',
    'pm2_5_volume_concentration',
    'precipitation',
    'rainfall',
    'rainfall_mass_rate',
    'rainfall_rate',
    'relative_humidity',
    'wind_speed',
    #
    # snow ----------------------------------------------
    'snow_coverage',
    'snowfall_water_equivalent',
    'snow_depth_water_equivalent',
    'snow_depth',
    'snow_loss_energy',
    'snow_loss_factor',
    'snowfall',
    'snow_density',
    'snowfall_mass_rate',
    'snowfall_rate',
    #
    # soiling -------------------------------------------
    'soiling_mass',
    'soiling_level',
    'soiling_level_value',
    'soiling_rate',
    'soiling_rate_value',
    'soiling_ratio',
    #
    # other ---------------------------------------------
    'completeness',
    'coverage',
    'distance',
    'score',
    'any',
    # PVGIS tables --------------------------------------
    'pvgis_seriescalc_table',  # https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en
    #
    # ERA5 collections (tables) -------------------------
    'era5_single_level_table',  # https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
    #
    # MERRA2 collections (tables) -----------------------
    'merra2_aerosol_mixing_table',  # M2I3NVAER, Aerosol Mixing Ratio
    'merra2_surface_flux_table',  # M2T1NXFLX, Surface Flux Diagnostics
    'merra2_meteo_table',  # M2I1NXASM, Single-Level Diagnostics
    'merra2_land_surface_table',  # M2T1NXLND, Land Surface Diagnostics
    #
    # Other tables
    'meteo_station_table',  # e.g. NOAA meteo stations, but can also be from other sources
]


def is_pvradar_resource_type(value: Any) -> TypeGuard[PvradarResourceType]:
    return value in get_args(PvradarResourceType.__value__)


class BaseResourceAttrs(TypedDict):
    resource_type: NotRequired[str]


class ModelParamAttrs(BaseResourceAttrs):
    """Parameter attrs, also used in .resource() call"""

    to_unit: NotRequired[str]
    set_unit: NotRequired[str]
    to_freq: NotRequired[str]
    agg: NotRequired[AggFunctionName]

    measurement_id: NotRequired[str]
    source_id: NotRequired[str]

    keep: NotRequired[bool]

    params: NotRequired[Mapping[str, Any]]


class Attrs(ModelParamAttrs):
    """PVRADAR-specific attrs that use pvradar_resource_type unlike a generic resource_type"""

    resource_type: NotRequired[PvradarResourceType]  # type: ignore
    datasource: NotRequired[Datasource]


def attrs(
    *,
    to_unit: Optional[str] = None,
    set_unit: Optional[str] = None,
    to_freq: Optional[str] = None,
    agg: Optional[AggFunctionName] = None,
    measurement_id: Optional[str] = None,
    source_id: Optional[str] = None,
    keep: Optional[bool] = None,
    params: Optional[Mapping[str, Any]] = None,
    resource_type: Optional[PvradarResourceType] = None,
    datasource: Optional[Datasource] = None,
) -> Attrs:
    result = {}
    if to_unit is not None:
        result['to_unit'] = to_unit
    if set_unit is not None:
        result['set_unit'] = set_unit
    if to_freq is not None:
        result['to_freq'] = to_freq
    if agg is not None:
        result['agg'] = agg
    if measurement_id is not None:
        result['measurement_id'] = measurement_id
    if source_id is not None:
        result['source_id'] = source_id
    if keep is not None:
        result['keep'] = keep
    if params is not None:
        result['params'] = params
    if resource_type is not None:
        result['resource_type'] = resource_type
    if datasource is not None:
        result['datasource'] = datasource
    return result  # type: ignore


class SeriesAttrs(BaseResourceAttrs):
    freq: NotRequired[str]
    unit: NotRequired[str]
    agg: NotRequired[AggFunctionName]


class FrameAttrs(BaseResourceAttrs):
    freq: NotRequired[str]


class ModelConfig(TypedDict):
    disable_validation: NotRequired[bool]  # e.g. validation of attrs in model params
    disable_auto_resolve: NotRequired[bool]  # if true then context['model_name'] will NOT be resolved as ModelBinding
    ignore_missing_params: NotRequired[bool]  # model will be executed (run) even if some params are missing


class ModelRecipe(TypedDict):
    model_name: str
    params: NotRequired[Mapping[str, Any]]


class BindingNotFound:
    def __init__(self, reason: str = '') -> None:
        self.reason = reason

    @classmethod
    def check(cls, subject: Any) -> bool:
        return subject is BindingNotFound or isinstance(subject, cls)


class EmptyBinding:
    """marker object for binding returning None"""


@dataclass
class ModelParam:
    name: str
    annotation: Any
    attrs: Optional[Mapping[str, Any]] = None
    default: Optional[Any] = inspect.Parameter.empty
    type: Type = NoneType

    def __repr__(self) -> str:
        result = str(self.annotation)
        if self.default != inspect.Parameter.empty:
            if result.endswith('>'):
                result = result[:-1]
            result += f' = {self.default}'
        if result.startswith('<') and not result.endswith('>'):
            result += '>'
        return result


@dataclass
class Audience:
    any_org: bool = False
    org_ids: list[str] = field(default_factory=list)
    project_goals: list[str] = field(default_factory=list)
