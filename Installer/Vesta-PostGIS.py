#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
'''
Created on 08/04/2013

@author: vladimir
'''
import logging
import traceback
import sys
import subprocess

from GraphicProduct import GraphicProduct
RADAR_ID = 'CCMW'


if __name__ == '__main__':
    loglevel = "WARNING"
    for arg in sys.argv:
        if str(arg[2:5]).lower() == "log":
            loglevel = arg[6:]
                     
        if str(arg[1:2]).lower() == "f":
            filename = arg[3:] 
            
        if str(arg[1:2]).lower() == "s":
            RADAR_ID = arg[3:] 
            
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    
    log_format = "%(levelname)s | %(asctime)s | %(name)s | %(message)s"
    logging.basicConfig(filename="vesta_postgis.log", level=numeric_level, 
                        format=log_format, datefmt='%H:%M:%S %d/%m/%Y')
    logger = logging.getLogger("Vesta-PostGIS")
    
    logger.debug("Initializing Vesta-PostGIS...")
    
    try:
        gp = GraphicProduct(filename, 'products_properties.xml', RADAR_ID)
        gp.upload()
	subprocess.getoutput('rm %s' % filename)
    except:        
        class Myfile:
            def __init__(self):
                pass
            def write(self,txt):
                logger.error(txt)
        logger_file = Myfile()
        traceback.print_exc(file = logger_file)
        
        
