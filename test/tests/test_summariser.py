#!/usr/bin/env python

import xarray

method = 'daymean'

infiles = []
outfiles = []

start_year = 2000
end_year = 2000
years = [
    str(num) for num in range(
        int(start_year),
        int(end_year) + 1
    )
]
months = [
    str(num).zfill(2) for num in range(1, 13)    
]

regrid_directory = '/home/simon/dev/era5toolbox/test/data/regrid'
summary_directory = '.'
region_name = 'india'
variable = 'total_precipitation'
infiles = []
outfiles = []
method = 'daysum'

for year in years:
    for month in months:
        infiles.append(
            os.path.join(
                regrid_directory,
                'era5_reanalysis_'
                + variable + '_'
                + region_name + '_'
                + year + month + '.nc'
            )
        )
        outfiles.append(
            os.path.join(
                summary_directory,
                'era5_reanalysis_'
                + variable + '_'
                + region_name + '_'
                + method + '_'
                + year + month + '.nc'
            )
        )

    ds = xarray.open_mfdataset(infiles, combine='by_coords')
    # remove first time
    ds = ds.isel(time=[i for i in range(1, ds.time.size)])
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
