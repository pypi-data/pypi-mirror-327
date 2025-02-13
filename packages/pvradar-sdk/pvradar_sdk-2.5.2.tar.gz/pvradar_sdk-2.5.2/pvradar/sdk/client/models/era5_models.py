from typing import Any, Annotated as A
import pandas as pd

from ..api_query import Query
from ..client import PvradarClient
from pvlib.location import Location
from ...modeling.decorators import datasource, pvradar_resource_type
from ...modeling.utils import auto_attr_table, convert_series_unit
from ..pvradar_resources import pvradar_resource_annotations, SeriesConfigAttrs as S
from ...modeling.basics import Attrs as P


era5_series_name_mapping: dict[str, str | A[Any, Any]] = {
    # ----------------------------------------------------
    # Single levels
    #
    '2m_temperature': A[pd.Series, S(resource_type='air_temperature', unit='degK', agg='mean', freq='1h')],
    'snow_depth': A[
        pd.Series, S(resource_type='snow_depth_water_equivalent', unit='m', agg='mean', freq='1h')
    ],  # snow_depth_water
    'snowfall': A[pd.Series, S(resource_type='snowfall_water_equivalent', unit='m', agg='sum', freq='1h')],  # snowfall_water
    'snow_density': A[pd.Series, S(resource_type='snow_density', unit='kg/m^3', agg='mean', freq='1h')],
    # ----------------------------------------------------
    # Pressure levels
    'relative_humidity': A[pd.Series, S(resource_type='relative_humidity', unit='%', agg='mean', freq='1h')],
}


def _auto_attr_table(df: pd.DataFrame, **kwargs) -> None:
    if df is None:
        return
    auto_attr_table(
        df,
        series_name_mapping=era5_series_name_mapping,
        resource_annotations=pvradar_resource_annotations,
        **kwargs,
    )
    for name in df:
        df[name].attrs['datasource'] = 'era5'


# ----------------------------------------------------
# ERA5 tables


@pvradar_resource_type('era5_single_level_table')
@datasource('era5')
def era5_single_level_table(
    location: Location,
    interval: pd.Interval,
) -> pd.DataFrame:
    query = Query.from_site_environment(location=location, interval=interval)
    query.set_path('datasources/era5/raw/hourly/csv')
    result = PvradarClient.instance().get_df(query, crop_interval=interval)
    _auto_attr_table(result)
    return result


# ----------------------------------------------------
# ERA5 series (alphabetical order)


@pvradar_resource_type('air_temperature', rename=True)
@datasource('era5')
def era5_air_temperature(
    *,
    era5_single_level_table: A[pd.DataFrame, P(resource_type='era5_single_level_table')],
) -> pd.Series:
    return convert_series_unit(era5_single_level_table['2m_temperature'], to_unit='degC')


@pvradar_resource_type('relative_humidity', rename=True)
@datasource('era5')
def era5_relative_humidity(
    *,
    era5_single_level_table: A[pd.DataFrame, P(resource_type='era5_single_level_table')],
) -> pd.Series:
    series = era5_single_level_table['relative_humidity']
    if series.attrs['unit'] != '%':
        raise ValueError(f'Unexpected unit: {series.attrs["unit"]}')
    return series.copy()


@pvradar_resource_type('snow_density', rename=True)
@datasource('era5')
def era5_snow_density(
    *,
    era5_single_level_table: A[pd.DataFrame, P(resource_type='era5_single_level_table')],
) -> pd.Series:
    series = era5_single_level_table['snow_density']
    if series.attrs['unit'] != 'kg/m^3':
        raise ValueError(f'Unexpected unit: {series.attrs["unit"]}')
    return series.copy()


@pvradar_resource_type('snow_depth_water_equivalent', rename=True, use_std_unit=True)
@datasource('era5')
def era5_snow_depth_water_equivalent(
    *,
    era5_single_level_table: A[pd.DataFrame, P(resource_type='era5_single_level_table')],
) -> pd.Series:
    result = era5_single_level_table['snow_depth']
    # unit conversion done automatically
    result.attrs['resource_type'] = 'snow_depth'
    return result


@pvradar_resource_type('snow_depth', rename=True, use_std_unit=True)
@datasource('era5')
def era5_snow_depth(
    *,
    era5_snow_depth_water_equivalent: A[pd.Series, P(resource_type='snow_depth_water_equivalent', datasource='era5')],
    snow_density: A[pd.Series, P(resource_type='snow_density', datasource='era5')],
) -> pd.Series:
    result = era5_snow_depth_water_equivalent * (1000 / snow_density)
    result.attrs['agg'] = 'mean'
    return result


@pvradar_resource_type('snowfall_water_equivalent', rename=True, use_std_unit=True)
@datasource('era5')
def era5_snowfall_water_equivalent(
    *,
    era5_single_level_table: A[pd.DataFrame, P(resource_type='era5_single_level_table')],
) -> pd.Series:
    result = era5_single_level_table['snowfall']
    # unit conversion done automatically
    result.attrs['resource_type'] = 'snowfall'
    return result


@pvradar_resource_type('snowfall', rename=True, use_std_unit=True)
@datasource('era5')
def era5_snowfall(
    *,
    era5_snowfall_water_equivalent: A[pd.Series, P(resource_type='snowfall_water_equivalent', datasource='era5')],
) -> pd.Series:
    snow_density_value = 100  # Kg/m^3, value for fresh snow
    result = era5_snowfall_water_equivalent * (1000 / snow_density_value)
    result.attrs['agg'] = 'sum'
    return result
