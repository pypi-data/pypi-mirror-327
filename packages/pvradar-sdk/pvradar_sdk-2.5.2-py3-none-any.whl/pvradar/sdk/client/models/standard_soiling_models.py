


# @resource_type('particle_volume_concentration_table')
# def std_soiling_particle_volume_concentration_table(
#     location: Location,
#     interval: pd.Interval,
#     particle_names: list[str],
# ) -> pd.DataFrame:
#     query = Query.from_site_environment(location=location, interval=interval)
#     query.set_path('standard-soiling/volume-concentration/daily/csv')
#     query['particles'] = ','.join(particle_names)
#     result = PvradarClient.instance().get_df(query)

#     for particle_name in particle_names:
#         result[particle_name].attrs['unit'] = 'kg/m^3'
#         result[particle_name].attrs['particle_name'] = 'particle_name'

#     return result


# @resource_type('particle_volume_concentration')
# @to_unit('kg/m^3')
# def std_soiling_particle_volume_concentration(
#     location: Location,
#     interval: pd.Interval,
#     particle_name: str,
# ) -> pd.Series:
#     df = std_soiling_particle_volume_concentration_table(location, interval, [particle_name])
#     series = df[particle_name]
#     return series
