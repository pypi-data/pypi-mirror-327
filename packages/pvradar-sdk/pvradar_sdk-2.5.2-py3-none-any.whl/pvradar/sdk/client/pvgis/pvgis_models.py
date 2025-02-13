from typing import Any, Annotated as A, Optional
import pandas as pd
from pydantic import Field

from .pvgis_client import PvgisClient, PvgisSeriescalcParams, PvgisDatabase, pvgis_csv_to_pandas
from ...common.pandas_utils import crop_by_interval
from ...modeling.basics import attrs
from pvlib.location import Location
from ...modeling.decorators import datasource, pvradar_resource_type
from ...modeling.utils import auto_attr_table
from ..pvradar_resources import SeriesAttrs, pvradar_resource_annotations, SeriesConfigAttrs as S


pvgis_series_name_mapping: dict[str, str | A[Any, SeriesAttrs]] = {
    'G(i)': A[pd.Series, S(resource_type='global_horizontal_irradiance', unit='W/m^2', agg='mean', freq='1h')],
    'H_sun': A[pd.Series, S(resource_type='solar_elevation_angle', unit='deg', agg='mean', freq='1h')],
    'T2m': A[pd.Series, S(resource_type='air_temperature', unit='degC', agg='mean', freq='1h')],
    'WS10m': A[pd.Series, S(resource_type='wind_speed', unit='m/s', agg='mean', freq='1h')],
}


def _auto_attr_table(df: pd.DataFrame, **kwargs) -> None:
    if df is None:
        return
    auto_attr_table(
        df,
        series_name_mapping=pvgis_series_name_mapping,
        resource_annotations=pvradar_resource_annotations,
        **kwargs,
    )
    for name in df:
        df[name].attrs['datasource'] = 'pvgis'


# ----------------------------------------------------
# PVGIS tables


@pvradar_resource_type('pvgis_seriescalc_table')
@datasource('pvgis')
def pvgis_seriescalc_table(
    *,
    location: A[Location, Field()],
    interval: A[pd.Interval, Field()],
    pvgis_database: Optional[PvgisDatabase] = None,
    tz: Optional[str] = None,
) -> pd.DataFrame:
    query: PvgisSeriescalcParams = {
        'lon': location.longitude,
        'lat': location.latitude,
        'startyear': interval.left.tz_convert('utc').year,
        'endyear': interval.right.tz_convert('utc').year,
    }
    if pvgis_database is not None:
        query['raddatabase'] = pvgis_database
    response = PvgisClient.instance().get_seriescalc(query)
    result = pvgis_csv_to_pandas(response, tz=tz if tz is not None else location.tz)
    returned_pvgis_database = result.attrs.get('pvgis_database')
    result = crop_by_interval(result, interval)
    _auto_attr_table(result)
    if returned_pvgis_database is not None:
        result.attrs['pvgis_database'] = returned_pvgis_database
        for name in result:
            result[name].attrs['pvgis_database'] = returned_pvgis_database
    return result


# ----------------------------------------------------
# PVGIS series (alphabetical order)


@pvradar_resource_type('air_temperature', rename=True)
@datasource('pvgis')
def pvgis_air_temperature(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, attrs(resource_type='pvgis_seriescalc_table')],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['T2m']


@pvradar_resource_type('global_horizontal_irradiance', rename=True)
@datasource('pvgis')
def pvgis_global_horizontal_irradiance(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, attrs(resource_type='pvgis_seriescalc_table')],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['G(i)']


@pvradar_resource_type('solar_elevation_angle', rename=True)
@datasource('pvgis')
def pvgis_solar_elevation_angle(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, attrs(resource_type='pvgis_seriescalc_table')],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['H_sun']


@pvradar_resource_type('wind_speed', rename=True)
@datasource('pvgis')
def pvgis_wind_speed(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, attrs(resource_type='pvgis_seriescalc_table')],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['WS10m']
