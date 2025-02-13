import csv
from io import StringIO
from typing import TypeGuard, TypeVar
from pandas import DataFrame, DatetimeIndex, Series, Interval, Timestamp, date_range, read_csv, to_datetime
from dataclasses import dataclass

SeriesOrFrame = TypeVar('SeriesOrFrame', Series, DataFrame)


def is_series_or_frame(obj: object) -> TypeGuard[SeriesOrFrame]:
    return isinstance(obj, Series) or isinstance(obj, DataFrame)


@dataclass
class UnitConversion:
    suffix: str
    factor: float


field_map = {
    'distance': UnitConversion('km', 1e-3),
}

exclude_rounding = ['lat', 'lon']


def process_df(df: DataFrame, precise: bool = False, convert_units: bool = True) -> DataFrame:
    copy_made = False
    if convert_units:
        df = df.copy(deep=True)
        copy_made = True
        for key in field_map.keys():
            if key in df.columns:
                new_key = key + '_' + field_map[key].suffix
                df[new_key] = df[key] * field_map[key].factor
                df.drop(columns=[key], inplace=True)

    if not precise:
        if not copy_made:
            df = df.copy(deep=True)
        float_columns = df.select_dtypes(include='float').columns
        columns_to_round = [col for col in float_columns if col not in exclude_rounding]
        df[columns_to_round] = df[columns_to_round].round(2)
    return df


def api_csv_string_to_df(csv_str: str, tz: str | None = None) -> DataFrame:
    if csv_str.strip() == '':
        # Return empty DataFrame if the CSV string is empty
        return DataFrame()
    header = next(csv.reader(StringIO(csv_str)))
    df = read_csv(StringIO(csv_str))

    if header[0] in ['isoDate', 'iso_date']:
        iso_date = to_datetime(df[header[0]])
        if iso_date.dt.tz is None:
            # ATTENTION: quickfix, unclear why we need it
            iso_date = iso_date.dt.tz_localize('UTC')
        try:
            df[header[0]] = iso_date if tz is None else iso_date.dt.tz_convert(tz)
        except Exception as e:
            raise RuntimeError(f'Error converting date to timezone: {e}')
        index_name = header[0]
        if 'forecast_hour' in df.columns:
            index_name = [index_name, 'forecast_hour']
        df.set_index(index_name, inplace=True)

    if header[0] == 'month' and len(df) == 12:
        df.set_index(header[0], inplace=True)
    return df


def crop_by_interval(df: SeriesOrFrame, interval: Interval) -> SeriesOrFrame:
    assert isinstance(interval, Interval)
    assert isinstance(interval.left, Timestamp)
    assert isinstance(interval.right, Timestamp)
    if isinstance(df, Series):
        return df.loc[interval.left : interval.right]
    if isinstance(df, DataFrame):
        # workaround for bug in pandas overwriting attrs
        result = df.loc[interval.left : interval.right]
        for column in df.columns:
            result[column].attrs = df[column].attrs
        return result
    raise ValueError(f'crop_by_interval supports only Series or DataFrame, got {type(df)}')


def interval_to_index(interval: Interval, freq: str = '1h') -> DatetimeIndex:
    return date_range(start=interval.left, end=interval.right, freq=freq)
