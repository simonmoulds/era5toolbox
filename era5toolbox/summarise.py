#!/usr/bin/env python

import os

class SummariseERA5(object):
    def __init__(self, config):
        self.config = config

    def summarise(self):
        pass

# datadir=$HOME/data/ERA5
# outdir=/mnt/scratch/scratch/data/ERA5
# if [ ! -d $outdir ]
# then
#     mkdir $outdir
# fi

# # Variables:
# # ===========================================================
# # u10      | 10 metre U wind component    | m s-1
# # v10      | 10 metre V wind component    | m s-1
# # d2m      | 2 metre dewpoint temperature | K
# # t2m      | 2 metre temperature          | K
# # sp       | Surface pressure             | Pa
# # msl      | Mean sea level pressure      | Pa
# # msdwlwrf | Mean surface downward long-wave radiation flux  | W m-2
# # msdwswrf | Mean surface downward short-wave radiation flux | W m-2
# # msnlwrf  | Mean surface net long-wave radiation flux | W m-2
# # msnswrf  | Mean surface net short-wave radiation flux | W m-2
# # ssrd     | Surface solar radiation downwards | J m-2
# # tp       | Total precipitation               | m
# # str      | Surface net thermal radiation | J m-2
# # tcc      | Total cloud cover             | (0 - 1)

# for year in {1979..2019}
# do
#     for month in {01..12}
#     do
	
# 	# ################################################# #
# 	# 10m u component of wind (m s-1)
# 	# ################################################# #

# 	cdo \
# 	    select,name=u10 \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_10m_u_component_of_wind_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_10m_u_component_of_wind_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_10m_u_component_of_wind_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# 10m v component of wind
# 	# ################################################# #
# 	cdo \
# 	    select,name=v10 \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_10m_v_component_of_wind_${year}${month}.nc	
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_10m_v_component_of_wind_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_10m_v_component_of_wind_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# 2m dewpoint temperature
# 	# ################################################# #
# 	cdo \
# 	    select,name=d2m \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_2m_dewpoint_temperature_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_2m_dewpoint_temperature_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_2m_dewpoint_temperature_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# 2m temperature
# 	# ################################################# #
# 	cdo \
# 	    select,name=t2m \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_2m_temperature_${year}${month}.nc
	
# 	# # convert from Kelvin to degrees centigrade
# 	# cdo \
# 	#     -b 64 addc,-273.15 \
# 	#     ${outdir}/era5_reanalysis_2m_temperature_${year}${month}.nc \
# 	#     ${outdir}/era5_reanalysis_2m_temperature_degC_${year}${month}.nc
# 	# ncatted \
# 	#     -a units,t2m,o,c,'degree_Celsius' \
# 	#     ${outdir}/era5_reanalysis_2m_temperature_degC_${year}${month}.nc
	
# 	cdo \
# 	    -b 64 daymin \
# 	    ${outdir}/era5_reanalysis_2m_temperature_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_2m_temperature_daymin_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymax \
# 	    ${outdir}/era5_reanalysis_2m_temperature_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_2m_temperature_daymax_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_2m_temperature_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_2m_temperature_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# Surface pressure
# 	# ################################################# #
# 	cdo \
# 	    select,name=sp \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_surface_pressure_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_surface_pressure_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_surface_pressure_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# Mean sea level pressure
# 	# ################################################# #
# 	cdo \
# 	    select,name=msl \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_sea_level_pressure_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_mean_sea_level_pressure_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_sea_level_pressure_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# Mean surface downward longwave radiation flux
# 	# ################################################# #
# 	cdo \
# 	    select,name=msdwlwrf \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_downward_long_wave_radiation_flux_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_mean_surface_downward_long_wave_radiation_flux_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_downward_long_wave_radiation_flux_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# Mean surface downward shortwave radiation flux
# 	# ################################################# #
# 	cdo \
# 	    select,name=msdwswrf \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_downward_short_wave_radiation_flux_${year}${month}.nc
# 	cdo -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_mean_surface_downward_short_wave_radiation_flux_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_downward_short_wave_radiation_flux_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# Mean surface net longwave radiation flux
# 	# ################################################# #
# 	cdo \
# 	    select,name=msnlwrf \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_net_long_wave_radiation_flux_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_mean_surface_net_long_wave_radiation_flux_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_net_long_wave_radiation_flux_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# Mean surface net shortwave radiation flux
# 	# ################################################# #
# 	cdo \
# 	    select,name=msnswrf \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_net_short_wave_radiation_flux_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_mean_surface_net_short_wave_radiation_flux_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_mean_surface_net_short_wave_radiation_flux_daymean_${year}${month}.nc

# 	# ################################################# #
# 	# Surface solar radiation downwards
# 	# ################################################# #
# 	cdo \
# 	    select,name=ssrd \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_surface_solar_radiation_downwards_${year}${month}.nc
# 	cdo \
# 	    -b 64 daysum \
# 	    ${outdir}/era5_reanalysis_surface_solar_radiation_downwards_${year}${month}.nc\
# 	    ${outdir}/era5_reanalysis_surface_solar_radiation_downwards_daysum_${year}${month}.nc

# 	# ################################################# #
# 	# Total precipitation
# 	# ################################################# #
# 	cdo \
# 	    select,name=tp \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_total_precipitation_${year}${month}.nc
# 	cdo \
# 	    -b 64 daysum \
# 	    ${outdir}/era5_reanalysis_total_precipitation_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_total_precipitation_daysum_${year}${month}.nc

# 	# ################################################# #
# 	# Surface net thermal radiation
# 	# ################################################# #
# 	cdo \
# 	    select,name=str \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_surface_net_thermal_radiation_${year}${month}.nc
# 	cdo \
# 	    -b 64 daysum \
# 	    ${outdir}/era5_reanalysis_surface_net_thermal_radiation_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_surface_net_thermal_radiation_daysum_${year}${month}.nc

# 	# ################################################# #
# 	# Total cloud cover
# 	# ################################################# #
# 	cdo \
# 	    select,name=tcc \
# 	    ${datadir}/era5_reanalysis_${year}${month}.nc \
# 	    ${outdir}/era5_reanalysis_total_cloud_cover_${year}${month}.nc
#         # cdo \
# 	#     setunit,'oktas' \
# 	#     -expr,'tcco=tcc*100/12.5' \
# 	#     ${outdir}/era5_reanalysis_total_cloud_cover_${year}${month}.nc \
# 	#     ${outdir}/era5_reanalysis_total_cloud_cover_oktas_${year}${month}.nc
# 	# ncatted \
# 	#     -a standard_name,tcco,o,c,'cloud_area_fraction' \
# 	#     ${outdir}/era5_reanalysis_total_cloud_cover_oktas_${year}${month}.nc
# 	# ncatted \
# 	#     -a long_name,tcco,o,c,'Total cloud cover in oktas' \
# 	#     ${outdir}/era5_reanalysis_total_cloud_cover_oktas_${year}${month}.nc
# 	cdo \
# 	    -b 64 daymean \
# 	    ${outdir}/era5_reanalysis_total_cloud_cover_oktas_${year}${month}.nc \
# 	    ${outdir}/tmp.nc
# 	cdo \
# 	    shifttime,-690min \
# 	    ${outdir}/tmp.nc \
# 	    ${outdir}/era5_reanalysis_total_cloud_cover_oktas_daymean_${year}${month}.nc
#     done
# done
