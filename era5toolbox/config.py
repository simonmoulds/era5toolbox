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

class Config(object):
    def __init__(self, config_filename):
        config_filename = os.path.abspath(config_filename)
        self.parse_config_file()

    def parse_config_file(self):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.optionxform = str
        config.read(os.path.abspath(sys.argv[1]))

        self.download_directory = config.get('FILE_PATHS', 'download_directory')
        self.regrid_directory = config.get('FILE_PATHS', 'regrid_directory')
        self.summary_directory = config.get('FILE_PATHS', 'summary_directory')

        self.start_year = config.get('TIME', 'start')
        self.end_year = config.get('TIME', 'end')
        self.download = bool(int(config.get('TASKS', 'download')))
        self.regrid = bool(int(config.get('TASKS', 'regrid')))
        self.summarise = bool(int(config.get('TASKS', 'aggregate')))
        self.specifichumidity = bool(int(config.get('TASKS', 'specifichumidity')))

        self.region_name = config.get('AREA', 'name')
        self.area = [
            float(config.get('AREA', 'north')),
            float(config.get('AREA', 'west')),
            float(config.get('AREA', 'south')),
            float(config.get('AREA', 'east')),        
        ]
        self.resolution = 0.25

        variables = []
        for variable in VARIABLES:
            if variable in config.options('VARIABLES'):
                include = bool(int(config.get('VARIABLES', variable)))
                if include:
                    variables.append(variable)
        self.variables = variables
        
