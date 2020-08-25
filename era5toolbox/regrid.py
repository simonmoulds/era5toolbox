#!/usr/bin/env python

import os
import sys
import tempfile
import subprocess
from .config import Config
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
            'grid_' + self.config.region_name + '_'
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
                infile = os.path.join(
                    self.config.download_directory,
                    'era5_reanalysis_'
                    + self.config.region_name + '_' \
                    + str(self.config.file_prefix) \
                    + year + month + '.nc'
                )
                
                # loop through the variables, select, regrid
                for variable in self.config.regrid_variables:
                    tmpfile1 = tempfile.NamedTemporaryFile(suffix='.nc')
                    tmpfile2 = tempfile.NamedTemporaryFile(suffix='.nc')
                    outfile = os.path.join(
                        self.config.regrid_directory,
                        'era5_reanalysis_'
                        + variable + '_'
                        + self.config.region_name + '_'
                        + str(self.config.file_prefix) \
                        + year + month + '.nc'
                    )

                    if not os.path.isfile(outfile):
                        try:
                            subprocess.run([
                                'cdo',
                                'select,name=' + VARNAMES[variable],
                                infile,
                                tmpfile1.name
                            ])
                        except KeyboardInterrupt:
                            break
                        try:
                            # use bilinear interpolation for all continuous variables
                            subprocess.run([
                                'cdo',
                                'remapbil,' + self.gridfile,
                                tmpfile1.name,
                                tmpfile2.name
                            ])
                            # ensure that variables have datatype 'double', not 'short', which seems to cause problems in JULES (not exactly sure why...)
                            subprocess.run([
                                'cdo',
                                '-b F64 copy',
                                tmpfile2.name,
                                outfile
                            ])
                        except KeyboardInterrupt:
                            break

def main():
    config = Config(os.path.abspath(sys.argv[1]))
    regridder = RegridERA5(config)
    regridder.regrid()

if __name__ == '__main__':
    main()
