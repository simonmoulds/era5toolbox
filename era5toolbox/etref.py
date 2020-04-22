#!/usr/bin/env python
# coding: utf-8

# compute hourly reference et

import os
import numpy as np
import netCDF4 as nc

datadir = "/home/sm510/data/ERA5"

def main():
    
    years = range(2010, 2020)
    months = range(1, 13)
    # years = range(2014, 2015)
    # months = range(12, 13)

    for year in years:
        for month in months:

            # open a dataset which we can use as a template
            yearmon = str(year) + str(month).zfill(2)
            tmp_filename = os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc')
            eto_filename = os.path.join(datadir, 'era5_reanalysis_fao_pm_eto_' + yearmon + '.nc')
            print('Writing file ' + eto_filename + '...')

            # ##########################################
            # 1 - copy dimension variables to a new file
            # ##########################################
            with nc.Dataset(tmp_filename) as src, nc.Dataset(eto_filename, 'w', clobber=True) as dst:
                # copy global attributes all at once via dictionary
                dst.setncatts(src.__dict__)
                # copy dimensions
                for name, dimension in src.dimensions.items():
                    dst.createDimension(
                        name, (len(dimension) if not dimension.isunlimited() else None))
                # copy all file data except for the excluded
                for name, variable in src.variables.items():
                    if name not in ['t2m','msnlwrf','msnswrf','sp','d2m','u10','v10','tp']:
                        x = dst.createVariable(name, variable.datatype, variable.dimensions)
                        # copy variable attributes all at once via dictionary
                        dst[name].setncatts(src[name].__dict__)        
                        dst[name][:] = src[name][:]

            # #########################
            # 2 - compute net radiation
            # #########################

            # net shortwave radiation (W m-2)
            nco = nc.Dataset(os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc'), 'r')        
            msnswrf = nco.variables['msnswrf'][:]
            nco.close()

            # net longwave radiation (W m-2)
            nco = nc.Dataset(os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc'), 'r')        
            msnlwrf = nco.variables['msnlwrf'][:]
            nco.close()

            # Conversion: 1 W = 1 J s-1
            # W m-2 -> MJ m-2 h-1
            msnswrf = msnswrf * 60 * 60 / 1e6
            msnlwrf = msnlwrf * 60 * 60 / 1e6
            rn = msnswrf + msnlwrf  # N.B. plus, because LW is -ve in ERA5

            # ground heat flux
            # during daytime: G_hr = 0.1 * Rn (45)
            # during night  : G_hr = 0.5 * Rn (46)
            daylight = msnswrf > 0.0
            g = np.zeros_like(rn)
            g[daylight] = (rn * 0.1)[daylight]
            g[np.logical_not(daylight)] = (rn * 0.5)[np.logical_not(daylight)]

            # #############################################
            # 3 - slope of saturation vapour pressure curve
            # #############################################

            nco = nc.Dataset(os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc'), 'r')
            t2m = nco.variables['t2m'][:]
            nco.close()

            t2m_degc = t2m - 273.15

            # Eq 13
            delta = (4098. * (0.6108 * np.exp((17.27 * t2m_degc) / (t2m_degc + 237.3)))) / ((t2m_degc + 237.3) ** 2)

            # ##########################
            # 4 - psychrometric constant
            # ##########################

            nco = nc.Dataset(os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc'), 'r')
            sp = nco.variables['sp'][:]
            nco.close()

            # Eq 8
            gamma = 0.665 * 1e-3 * sp * 1e-3

            # #################################################
            # 5 - saturation vapour pressure at air temperature
            # #################################################

            # Eq 11
            eo = 0.6108 * np.exp((17.27 * t2m_degc) / (t2m_degc + 237.3))

            # ##########################
            # 6 - actual vapour pressure
            # ##########################

            nco = nc.Dataset(os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc'), 'r')
            d2m = nco.variables['d2m'][:]
            nco.close()

            # Eq 54
            d2m_degc = d2m - 273.15
            ea = 0.6108 * np.exp((17.27 * d2m_degc) / (d2m_degc + 237.3))

            # ####################
            # 7 - wind speed at 2m
            # ####################

            # u-component of wind speed
            nco = nc.Dataset(os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc'), 'r')
            u10 = nco.variables['u10'][:]
            nco.close()        

            # v-component of wind speed
            nco = nc.Dataset(os.path.join(datadir, 'era5_reanalysis_' + yearmon + '.nc'), 'r')
            v10 = nco.variables['v10'][:]
            nco.close()

            u2 = u10 * 4.87 / (np.log(67.8 * 10 - 5.42))
            v2 = v10 * 4.87 / (np.log(67.8 * 10 - 5.42))

            # Pythagoras theorem
            ws2 = np.sqrt(u2 ** 2 + v2 ** 2)

            # ###################
            # 8 - Penman Monteith
            # ###################

            # Eq 53
            eto = (0.408 * delta * (rn - g) + gamma * (37. / (t2m + 273.15)) * ws2 * (eo - ea)) / (delta + gamma * (1. + 0.34 * ws2))
            eto[eto < 0.] = 0.

            # ######################
            # 9 - write data to file
            # ######################

            nco = nc.Dataset(eto_filename, 'r+', clobber=True)
            var = nco.createVariable(
                'eto',
                np.float64,
                ('time', 'latitude', 'longitude'),
                zlib=False)
            var.setncattr('standard_name', 'eto')
            var.setncattr('long_name', 'eto')
            var.setncattr('units','1')
            var[:] = eto
            nco.close()

if __name__ == '__main__':
    main()
