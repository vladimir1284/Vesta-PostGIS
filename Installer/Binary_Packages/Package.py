'''
Created on 31/03/2013

@author: vladimir
'''
import struct
import pyproj as pj  # @UnresolvedImport

RE = 8498666.67 # Radio equivalente de la Tierra (m)

# EPSG:2085 - Cuba Norte 
CUBAN_PJ = pj.Proj(proj="lcc", lat_1=22.35, lat_0=22.35, lon_0=-81, k_0=0.99993602,\
               x_0=500000, y_0=280296.016, ellps="clrk66", datum="NAD27", units="m")


class Package:
    '''
    Parent class for binary packages
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def plot(self, axes, plt):
        pass
        