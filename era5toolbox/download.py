#!/usr/bin/env python

# ========================================================= #
# ========================================================= #
#
# For guidance on how to download ERA5 data, see the
# following website:
# 
# https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5#HowtodownloadERA5-StepA:InstallCDSAPIonyourmachine
#
# To install the CDS API client, follow the guide:
#
# https://cds.climate.copernicus.eu/api-how-to
#
# Simon Moulds, April 2020
# 
# ========================================================= #
# ========================================================= #

import os
import cdsapi

c = cdsapi.Client()

MONTHS = [str(num).zfill(2) for num in range(1, 13)]
DAYS = [str(num).zfill(2) for num in range(1, 32)]
TIME = [(str(num).zfill(2) + ":00") for num in range(24)]

class DownloadERA5(object):
    def __init__(self, config):
        self.config = config

    def download(self):
        years = [
            str(num) for num in range(
                int(self.config.start_year),
                int(self.config.end_year) + 1
            )
        ]
        months = [
            str(num).zfill(2) for num in range(1, 13)
        ]
        for year in years:
            for month in months:
                fn = os.path.join(
                    self.config.download_directory,
                    'era5_reanalysis_' \
                    + self.config.region_name + '_' \
                    + year + month + '.nc'
                )
                # only download if the file doesn't already exist
                # (this should be an option)
                if not os.path.isfile(fn):
                    try:
                        c.retrieve(
                            'reanalysis-era5-single-levels',
                            {
                                'product_type' : 'reanalysis',
                                'format' : 'netcdf',
                                'area' : self.config.area,
                                'variable' : self.config.variables,
                                'year' : year,
                                'month' : month,
                                'day' : DAYS,
                                'time' : TIME
                            },
                            fn
                        )
                    except:
                        pass
        
# def main():
#     for year in YEARS:
#         for month in MONTHS:
#             fn = os.path.join(
#                 OUTDIR,
#                 'era5_reanalysis_' + REGION + '_' + year + month + '.nc'
#             )
#             try:
#                 c.retrieve(
#                     'reanalysis-era5-single-levels',
#                     {
#                         'product_type' : 'reanalysis',
#                         'format' : 'netcdf',
#                         'area' : AREA,
#                         'variable' : VARIABLES,
#                         'year' : year,
#                         'month' : month,
#                         'day' : DAYS,
#                         'time' : TIME
#                     },
#                     fn
#                 )
#             except:
#                 pass
            
# if __name__ == "__main__":
#     main()
