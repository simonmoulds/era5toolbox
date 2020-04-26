#!/usr/bin/env python

import os
import sys
import xarray
from .config import Config
from .constants import VARNAMES

# See discussion here for some background information on aggregating ERA5 data:
# https://confluence.ecmwf.int/pages/viewpage.action?pageId=149341027


class SummariseERA5(object):
    def __init__(self, config):
        self.config = config

    def summarise(self):
        if not os.path.isdir(self.config.summary_directory):
            os.mkdir(self.config.summary_directory)

        for variable in self.config.summary_variables:
            for method in self.config.summary_methods[variable]:
                infiles = []
                outfiles = []
                for year in self.config.years:
                    for month in self.config.months:
                        infiles.append(
                            os.path.join(
                                self.config.regrid_directory,
                                'era5_reanalysis_'
                                + variable + '_'
                                + self.config.region_name + '_'
                                + year + month + '.nc'
                            )
                        )
                        outfiles.append(
                            os.path.join(
                                self.config.summary_directory,
                                'era5_reanalysis_'
                                + variable + '_'
                                + self.config.region_name + '_'
                                + method + '_'
                                + year + month + '.nc'
                            )
                        )

                ds = xarray.open_mfdataset(infiles)
                
                # remove first time
                ds = ds.isel(time=[i for i in range(1, ds.time.size)])
                
                if method == 'daymean':
                    ds_aggr = ds.resample(
                        time='D', closed='right').mean(dim='time')
                elif method == 'daymax':
                    ds_aggr = ds.resample(
                        time='D', closed='right').max(dim='time')
                elif method == 'daymin':
                    ds_aggr = ds.resample(
                        time='D', closed='right').min(dim='time')
                elif method == 'daysum':
                    ds_aggr = ds.resample(
                        time='D', closed='right').sum(dim='time')

                import pandas as pd
                year_month_idx = pd.MultiIndex.from_arrays(
                    [ds_aggr['time.year'], ds_aggr['time.month']]
                )
                ds_aggr.coords['year_month'] = ('time', year_month_idx)
                _, datasets = zip(*ds_aggr.groupby('year_month'))
                
                # remove the year_month coordinate from each dataset    
                datasets = [d.drop('year_month') for d in datasets]
                xarray.save_mfdataset(datasets, outfiles)
                    
def main():
    config = Config(os.path.abspath(sys.argv[1]))
    Summariser = SummariseERA5(config)
    Summariser.Summarise()

if __name__ == '__main__':
    main()
