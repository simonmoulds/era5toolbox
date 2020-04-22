#!/usr/bin/env python

import os
import tempfile
import subprocess
import numpy as np
import xarray as xr
import metpy.calc as mpcalc

class SpecificHumidityERA5(object):
    def __init__(self, config):
        self.config = config

    def compute_specific_humidity(self):
        for year in self.config.years:
            for month in self.config.months:
                
                # construct filenames of dewpoint temperature and surface pressure
                d2mfn = os.path.join(
                    self.config.regrid_directory,
                    'era5_reanalysis_2m_dewpoint_temperature_' \
                    + self.config.region_name + '_' \
                    + year + month + '.nc'
                )
                spfn = os.path.join(
                    self.config.regrid_directory,
                    'era5_reanalysis_surface_pressure_' \
                    + self.config.region_name + '_' \
                    + year + month + '.nc'
                )
                
                # construct filename of output netCDF
                qfn = os.path.join(
                    self.config.regrid_directory,
                    'era5_reanalysis_specific_humidity_' \
                    + self.config.region_name + '_' \
                    + year + month + '.nc'
                )

                # perform calculation using MetPy (this should take care of units automatically)
                d2m = xr.open_dataset(d2mfn)
                sp = xr.open_dataset(spfn)
                q = mpcalc.specific_humidity_from_dewpoint(
                    d2m.d2m,
                    sp.sp
                )
                qxr = xr.DataArray(
                    np.array(q),
                    dims=d2m.d2m.dims,
                    coords=d2m.d2m.coords,
                    attrs={'units' : '1'}
                )
                qxr.to_netcdf(qfn)
