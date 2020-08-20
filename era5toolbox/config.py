#!/usr/bin/env python

import os
import sys
from configparser import ConfigParser, ExtendedInterpolation

VARIABLES = [
    '10m_u_component_of_wind',
    '10m_v_component_of_wind',
    '2m_dewpoint_temperature',
    '2m_temperature',
    'convective_precipitation',
    'convective_snowfall',
    'large_scale_precipitation',
    'large_scale_snowfall',
    'total_precipitation',
    'snowfall',
    'convective_rain_rate',
    'convective_snowfall_rate_water_equivalent',
    'large_scale_rain_rate',
    'large_scale_snowfall_rate_water_equivalent',
    'mean_sea_level_pressure',
    'surface_pressure',
    'mean_surface_downward_long_wave_radiation_flux',
    'mean_surface_downward_short_wave_radiation_flux',
    'mean_surface_net_long_wave_radiation_flux',
    'mean_surface_net_short_wave_radiation_flux',
    'surface_solar_radiation_downwards',
    'surface_thermal_radiation_downwards',
    'surface_net_thermal_radiation',
    'total_cloud_cover'
]

CDO_SUMMARY_METHODS = ['daymean', 'daymax', 'daymin']


class Config(object):
    def __init__(self, config_filename):
        config_filename = os.path.abspath(config_filename)
        self.parse_config_file()

    def parse_config_file(self):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.optionxform = str
        config.read(os.path.abspath(sys.argv[1]))

        self.download_directory = config.get(
            'FILE_PATHS', 'download_directory')
        self.regrid_directory = config.get('FILE_PATHS', 'regrid_directory')
        self.summary_directory = config.get('FILE_PATHS', 'summary_directory')
        try:
            self.file_prefix = config.get('FILE_PATHS', 'file_prefix')
        except:
            self.file_prefix = ''

        self.start_year = config.get('TIME', 'start')
        self.end_year = config.get('TIME', 'end')
        self.years = [
            str(num) for num in range(
                int(self.start_year),
                int(self.end_year) + 1
            )
        ]
        self.months = [
            str(num).zfill(2) for num in range(1, 13)
        ]

        self.download = bool(int(config.get('TASKS', 'download')))
        self.regrid = bool(int(config.get('TASKS', 'regrid')))
        self.summarise = bool(int(config.get('TASKS', 'aggregate')))
        self.specifichumidity = bool(
            int(config.get('TASKS', 'specifichumidity')))

        self.region_name = config.get('AREA', 'name')
        self.area = [
            float(config.get('AREA', 'north')),
            float(config.get('AREA', 'west')),
            float(config.get('AREA', 'south')),
            float(config.get('AREA', 'east')),
        ]
        self.resolution = 0.25

        self.download_variables = None
        if self.download:
            download_variables = []
            for variable in VARIABLES:
                if variable in config.options('DOWNLOAD'):
                    include = bool(int(config.get('DOWNLOAD', variable)))
                    if include:
                        download_variables.append(variable)
            self.download_variables = download_variables
        print(self.download_variables)
        
        self.regrid_variables = None
        if self.regrid:
            regrid_variables = []
            for variable in VARIABLES:
                if variable in config.options('REGRID'):
                    include = bool(int(config.get('REGRID', variable)))
                    if include:
                        regrid_variables.append(variable)
            self.regrid_variables = download_variables
        print(self.regrid_variables)
        
        self.summary_variables = None
        self.summary_methods = None
        if self.summarise:
            summary_variables = []
            summary_methods = {}
            for variable in VARIABLES:
                if variable in config.options('SUMMARY'):
                    method_str = str(config.get('SUMMARY', variable))
                    method = [str(val.strip())
                              for val in method_str.split(',')]
                    if all([m in CDO_SUMMARY_METHODS for m in method]):
                        summary_variables.append(variable)
                        summary_methods[variable] = method
                    else:
                        summary_methods[variable] = None

            self.summary_variables = summary_variables
            self.summary_methods = summary_methods
