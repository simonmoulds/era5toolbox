#!/usr/bin/env python

import os
import sys
from configparser import ConfigParser, ExtendedInterpolation

from .config import Config
from .download import DownloadERA5
from .regrid import RegridERA5
from .summarise import SummariseERA5

def main():

    config = Config(os.path.abspath(sys.argv[1]))
    if config.download:
        downloader = DownloadERA5(config)
        downloader.download()

    if config.regrid:
        regridder = RegridERA5(config)
        regridder.regrid()

    if config.specifichumidity:
        specifichumidity = SpecificHumidityERA5(config)
        specifichumidity.compute_specific_humidity()
        
    if config.summarise:
        summariser = SummariseERA5(config)
        summariser.summarise()
            
if __name__ == '__main__':
    main()
