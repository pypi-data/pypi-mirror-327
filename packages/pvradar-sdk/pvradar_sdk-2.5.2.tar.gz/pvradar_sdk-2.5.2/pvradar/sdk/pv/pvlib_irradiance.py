from typing import Literal, Annotated

from ..common.pandas_utils import interval_to_index
from ..modeling.model_context import ModelContext
from ..modeling.basics import Attrs
from pvlib.location import Location
from ..modeling.decorators import pvradar_resource_type, update_attrs
import pandas as pd
import numpy as np
import pvlib
from pvlib.tools import cosd
from pvlib import shading, irradiance

from .design import ArrayDesign, FixedStructureDesign, TrackerStructureDesign

### -------------------------- SOLAR POSITION -------------------------- ###


def _solar_position_table(
    location: Location,
    interval: pd.Interval,
):
    solar_position_table = location.get_solarposition(
        times=interval_to_index(interval),
        pressure=None,  # TODO: use actual pressure series
        temperature=12,  # TODO: use actual ambient temperature series
    )
    return solar_position_table


@pvradar_resource_type('solar_azimuth_angle', rename=True)
@update_attrs(unit='deg', agg='mean')
def solar_azimuth_angle(context: ModelContext) -> pd.Series:
    solar_pos_table = context.run(_solar_position_table)
    return solar_pos_table['azimuth']


@pvradar_resource_type('solar_elevation_angle', rename=True)
@update_attrs(unit='deg', agg='mean')
def solar_elevation_angle(context: ModelContext, apparent: bool = False) -> pd.Series:
    solar_pos_table = context.run(_solar_position_table)
    if apparent:
        return solar_pos_table['apparent_elevation']
    else:
        return solar_pos_table['elevation']


@pvradar_resource_type('solar_zenith_angle', rename=True)
@update_attrs(unit='deg', agg='mean')
def solar_zenith_angle(context: ModelContext, apparent: bool = False) -> pd.Series:
    solar_pos_table = context.run(_solar_position_table)
    if apparent:
        return solar_pos_table['apparent_zenith']
    else:
        return solar_pos_table['zenith']


### -------------------------- IRRADIANCE -------------------------- ###


@pvradar_resource_type('direct_normal_irradiance', rename=True)
@update_attrs(unit='W/m^2', agg='mean')
def direct_normal_irradiance(
    global_horizontal_irradiance: Annotated[pd.Series, Attrs(resource_type='global_horizontal_irradiance')],
    solar_zenith_angle: Annotated[pd.Series, Attrs(resource_type='solar_zenith_angle')],
    interval: pd.Interval,
) -> pd.Series:
    direct_normal_irradiance = pvlib.irradiance.dirint(
        ghi=global_horizontal_irradiance,
        solar_zenith=solar_zenith_angle,
        times=interval_to_index(interval),
        temp_dew=None,  # TODO: pass dew point temperature for correction
    )
    # pvlib.irradiance.dirint produces NaN when sun elevation < 0 meaning sun is under horizon line
    direct_normal_irradiance = direct_normal_irradiance.fillna(0)
    return direct_normal_irradiance


@pvradar_resource_type('diffuse_horizontal_irradiance', rename=True)
@update_attrs(unit='W/m^2', agg='mean')
def diffuse_horizontal_irradiance(
    global_horizontal_irradiance: Annotated[pd.Series, Attrs(resource_type='global_horizontal_irradiance')],
    direct_normal_irradiance: Annotated[pd.Series, Attrs(resource_type='direct_normal_irradiance')],
    solar_zenith_angle: Annotated[pd.Series, Attrs(resource_type='solar_zenith_angle')],
) -> pd.Series:
    irradiation_components_table = pvlib.irradiance.complete_irradiance(
        solar_zenith=solar_zenith_angle, ghi=global_horizontal_irradiance, dni=direct_normal_irradiance
    )
    return irradiation_components_table['dhi']


### -------------------------- ANGLE OF INCIDENCE -------------------------- ###


@pvradar_resource_type('tracker_rotation_angle', rename=True)
@update_attrs(unit='deg', agg='mean')
def tracker_rotation_angle(
    apparent_zenith: Annotated[pd.Series, Attrs(resource_type='solar_zenith_angle', params={'apparent': True})],
    apparent_azimuth: Annotated[pd.Series, Attrs(resource_type='solar_azimuth_angle')],
    array: ArrayDesign,
) -> pd.Series:
    """
    Determine the rotation angle of a single-axis tracker when given particular
    solar zenith and azimuth angles.

    Based on pvlib.tracking.singleaxis, but ...
    https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.tracking.singleaxis.html
    """

    tracker = array.structure
    assert isinstance(tracker, TrackerStructureDesign), 'Project needs to have a tracker structure.'

    # extract array design parameters
    axis_tilt = tracker.axis_tilt
    axis_azimuth = tracker.axis_azimuth
    max_angle = tracker.max_tracking_angle
    backtrack = tracker.backtracking
    gcr = array.ground_cover_ratio

    # calculate cross axis tilt
    cross_axis_tilt = pvlib.tracking.calc_cross_axis_tilt(
        slope_azimuth=array.slope_azimuth,
        slope_tilt=array.slope_tilt,
        axis_azimuth=tracker.axis_azimuth,
        axis_tilt=tracker.axis_tilt,
    )

    # The ideal tracking angle, omega_ideal, is the rotation to place the sun
    # position vector (xp, yp, zp) in the (x, z) plane, which is normal to
    # the panel and contains the axis of rotation. omega_ideal=0 indicates
    # that the panel is horizontal. Here, our convention is that a clockwise
    # rotation is positive, to view rotation angles in the same frame of
    # reference as azimuth. For example, for a system with tracking
    # axis oriented south, a rotation toward the east is negative, and a
    # rotation to the west is positive. This is a right-handed rotation
    # around the tracker y-axis.
    omega_ideal = shading.projected_solar_zenith_angle(
        axis_tilt=axis_tilt,
        axis_azimuth=axis_azimuth,
        solar_zenith=apparent_zenith,
        solar_azimuth=apparent_azimuth,
    )

    # filter for sun above panel horizon
    zen_gt_90 = apparent_zenith > 90
    omega_ideal[zen_gt_90] = np.nan

    # Account for backtracking
    if backtrack:
        # distance between rows in terms of rack lengths relative to cross-axis
        # tilt
        axes_distance = 1 / (gcr * cosd(cross_axis_tilt))

        # NOTE: account for rare angles below array, see GH 824
        temp = np.abs(axes_distance * cosd(omega_ideal - cross_axis_tilt))

        # backtrack angle using [1], Eq. 14
        with np.errstate(invalid='ignore'):
            omega_correction = np.degrees(-np.sign(omega_ideal) * np.arccos(temp))

        # NOTE: in the middle of the day, arccos(temp) is out of range because
        # there's no row-to-row shade to avoid, & backtracking is unnecessary
        # [1], Eqs. 15-16
        with np.errstate(invalid='ignore'):
            tracker_theta = omega_ideal + np.where(temp < 1, omega_correction, 0)
    else:
        tracker_theta = omega_ideal

    # Clip tracker_theta between the minimum and maximum angles.
    min_angle = -max_angle
    tracker_theta = np.clip(tracker_theta, min_angle, max_angle)  # type: ignore

    # replace missing values with night stow angle
    tracker_theta: pd.Series
    tracker_theta.fillna(tracker.night_stow_angle * (-1), inplace=True)
    # NOTE: multiplying with -1 to make tracker face east at night (random choice)
    # TODO: replace night stow tilt angle with night stow rotation angle (theta) to allow users
    # to define orientation towards west as well

    return tracker_theta


def tracker_orientation_table(
    tracker_rotation_angle: Annotated[pd.Series, Attrs(resource_type='tracker_rotation_angle')], array: ArrayDesign
) -> pd.DataFrame:
    """
    wrapper for pvlib funtion
    pvlib.tracking.calc_surface_orientation
    only for trackers
    Two columns:
    surface tilt
    surface azimuth
    """
    tracker = array.structure
    assert isinstance(tracker, TrackerStructureDesign)

    tracker_orientation_table: pd.DataFrame = pvlib.tracking.calc_surface_orientation(
        tracker_theta=tracker_rotation_angle,
        axis_tilt=tracker.axis_tilt,  # type: ignore
        axis_azimuth=tracker.axis_azimuth,  # type: ignore
    )

    return tracker_orientation_table  # type: ignore


def fixed_structure_orientation_table(array: ArrayDesign, interval: pd.Interval) -> pd.DataFrame:
    fixed = array.structure
    assert isinstance(fixed, FixedStructureDesign)
    fixed_structure_orientation_table = pd.DataFrame(
        {'surface_tilt': fixed.tilt, 'surface_azimuth': fixed.azimuth}, index=interval_to_index(interval)
    )
    return fixed_structure_orientation_table


@pvradar_resource_type('surface_tilt_angle', rename=True)
@update_attrs(unit='deg', agg='mean')
def surface_tilt_angle(context: ModelContext, array: ArrayDesign):
    if isinstance(array.structure, TrackerStructureDesign):
        orientation_table = context.run(tracker_orientation_table)
        return orientation_table['surface_tilt']

    else:
        orientation_table = context.run(fixed_structure_orientation_table)
        return orientation_table['surface_tilt']


@pvradar_resource_type('surface_azimuth_angle', rename=True)
@update_attrs(unit='deg', agg='mean')
def surface_azimuth_angle(context: ModelContext, array: ArrayDesign):
    if isinstance(array.structure, TrackerStructureDesign):
        orientation_table = context.run(tracker_orientation_table)
        return orientation_table['surface_azimuth']

    else:
        orientation_table = context.run(fixed_structure_orientation_table)
        return orientation_table['surface_azimuth']


@pvradar_resource_type('angle_of_incidence', rename=True)
@update_attrs(unit='deg', agg='mean')
def angle_of_incidence(
    surface_tilt: Annotated[pd.Series, Attrs(resource_type='surface_tilt_angle')],
    surface_azimuth: Annotated[pd.Series, Attrs(resource_type='surface_azimuth_angle')],
    apparent_solar_zenith: Annotated[pd.Series, Attrs(resource_type='solar_zenith_angle', params={'apparent': True})],
    solar_azimuth: Annotated[pd.Series, Attrs(resource_type='solar_azimuth_angle')],
):
    """
    Wrapper around irradiance.aoi
    """
    aoi = irradiance.aoi(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        solar_zenith=apparent_solar_zenith,
        solar_azimuth=solar_azimuth,
    )
    return aoi


### -------------------------- POA-IRRADIANCE -------------------------- ###

# ------ Resource Parameters

ModuleSide = Literal['both', 'front', 'back']

# ------ Plane Of Array Irradiance Components


def ground_reflected_on_front(
    surface_tilt: Annotated[pd.Series, Attrs(resource_type='surface_tilt_angle')],
    global_horizontal_irradiance: Annotated[pd.Series, Attrs(resource_type='global_horizontal_irradiance')],
    array: ArrayDesign,
) -> pd.Series:
    ground_reflected_on_front = pvlib.irradiance.get_ground_diffuse(
        surface_tilt=surface_tilt, ghi=global_horizontal_irradiance, albedo=array.albedo_value
    )
    return ground_reflected_on_front


def extraterrestrial_radiation(interval: pd.Interval) -> pd.Series:
    """
    The extraterrestrial solar radiation at the top of Earth's atmosphere accounting for
    Earth's orbital variations. Returns a series of values around 1300 - 1400 W/m^2.
    """
    timestamps = interval_to_index(interval)
    extraterrestrial_radiation = pvlib.irradiance.get_extra_radiation(datetime_or_doy=timestamps, method='spencer')
    return extraterrestrial_radiation  # type: ignore


def sky_diffuse_on_front(
    surface_tilt: Annotated[pd.Series, Attrs(resource_type='surface_tilt_angle')],
    surface_azimuth: Annotated[pd.Series, Attrs(resource_type='surface_azimuth_angle')],
    diffuse_horizontal_irradiance: Annotated[pd.Series, Attrs(resource_type='diffuse_horizontal_irradiance')],
    direct_normal_irradiance: Annotated[pd.Series, Attrs(resource_type='direct_normal_irradiance')],
    solar_zenith_angle: Annotated[pd.Series, Attrs(resource_type='solar_zenith_angle')],
    solar_azimuth_angle: Annotated[pd.Series, Attrs(resource_type='solar_azimuth_angle')],
    interval: pd.Interval,
) -> pd.Series:
    """
    Sum of isotropic, horizon, and circumsolar
    """
    irr_extraterrestrial = extraterrestrial_radiation(interval=interval)
    sky_diffuse_on_front = pvlib.irradiance.perez_driesse(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        dhi=diffuse_horizontal_irradiance,
        dni=direct_normal_irradiance,
        dni_extra=irr_extraterrestrial,
        solar_zenith=solar_zenith_angle,
        solar_azimuth=solar_azimuth_angle,
        airmass=None,
        return_components=False,
    )
    return sky_diffuse_on_front  # type: ignore


def direct_on_front(
    surface_tilt: Annotated[pd.Series, Attrs(resource_type='surface_tilt_angle')],
    surface_azimuth: Annotated[pd.Series, Attrs(resource_type='surface_azimuth_angle')],
    solar_zenith_angle: Annotated[pd.Series, Attrs(resource_type='solar_zenith_angle')],
    solar_azimuth_angle: Annotated[pd.Series, Attrs(resource_type='solar_azimuth_angle')],
    direct_normal_irradiance: Annotated[pd.Series, Attrs(resource_type='direct_normal_irradiance')],
) -> pd.Series:
    direct_on_front = pvlib.irradiance.beam_component(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        solar_zenith=solar_zenith_angle,
        solar_azimuth=solar_azimuth_angle,
        dni=direct_normal_irradiance,
    )
    return direct_on_front


@pvradar_resource_type('plane_of_array_irradiance', rename=True)
@update_attrs(unit='W/m^2', agg='mean')
def plane_of_array_irradiance(context: ModelContext, module_side: ModuleSide = 'front') -> pd.Series:
    """
    The global irradiance in the plane of the pv array.
    """

    if (module_side == 'both') or (module_side == 'front'):
        # irradiance on front side
        ground_reflected = context.run(ground_reflected_on_front)
        sky_diffuse = context.run(sky_diffuse_on_front)
        direct = context.run(direct_on_front)
        global_on_front = ground_reflected + sky_diffuse + direct
        global_on_front = global_on_front.fillna(0)

        if module_side == 'front':
            return global_on_front

    if (module_side == 'both') or (module_side == 'back'):
        # irradiance on back side
        raise NotImplementedError('Back side irradiance not implemented yet')

    global_on_both_sides = global_on_front  # + global_on_back

    return global_on_both_sides
