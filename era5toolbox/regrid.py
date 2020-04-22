#!/usr/bin/env python

import os
import tempfile
import subprocess
from .constants import VARNAMES

class RegridERA5(object):
    def __init__(self, config):
        self.config = config

    def write_cdo_gridfile(self):
        ymax = self.config.area[0]
        xmin = self.config.area[1]
        ymin = self.config.area[2]
        xmax = self.config.area[3]
        xsize = (xmax-xmin) / self.config.resolution
        ysize = (ymax-ymin) / self.config.resolution
        xfirst = xmin + self.config.resolution / 2.
        yfirst = ymax - self.config.resolution / 2.
        xinc = self.config.resolution
        yinc = -self.config.resolution
        self.gridfile = os.path.join(
            '/tmp',
            'grid_' + self.config.region_name + '_' \
            + '{:.6f}'.format(self.config.resolution) + 'Deg.txt'
        )
        f = open(self.gridfile, 'w')
        f.write('gridtype=lonlat\n')
        f.write('xsize=' + str(int(xsize)) + '\n')
        f.write('ysize=' + str(int(ysize)) + '\n')
        f.write('xfirst=' + str(xfirst) + '\n')
        f.write('xinc=' + str(xinc) + '\n')
        f.write('yfirst=' + str(yfirst) + '\n')
        f.write('yinc=' + str(yinc) + '\n')
        f.close()
        
    def regrid(self):
        self.write_cdo_gridfile()        
        # attempt to create output directory
        if not os.path.isdir(self.config.regrid_directory):
            os.mkdir(self.config.regrid_directory)            
        for year in self.config.years:
            for month in self.config.months:
                # filename of netCDF containing all variables
                fn = os.path.join(
                    self.config.download_directory,
                    'era5_reanalysis_' \
                    + self.config.region_name + '_' \
                    + year + month + '.nc'
                )
                # loop through the variables, select, regrid
                for variable in self.config.variables:
                    tmpfn = tempfile.NamedTemporaryFile(suffix='.nc')
                    newfn = os.path.join(
                        self.config.regrid_directory,
                        'era5_reanalysis_' \
                        + variable + '_' \
                        + self.config.region_name + '_' \
                        + year + month + '.nc'
                    )
                    
                    if not os.path.isfile(newfn):
                        try:
                            subprocess.run([
                                'cdo',
                                'select,name=' + VARNAMES[variable],
                                fn,
                                tmpfn.name
                            ])
                        except KeyboardInterrupt:
                            break
                        try:
                            subprocess.run([
                                'cdo',
                                'remapbil,' + self.gridfile,
                                tmpfn.name,
                                newfn
                            ])
                        except KeyboardInterrupt:
                            break
