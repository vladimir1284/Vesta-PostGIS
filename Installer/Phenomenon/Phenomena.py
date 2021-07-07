'''
Created on 11/04/2013

@author: vladimir
'''

import pyproj as pj  # @UnresolvedImport
import logging

logger = logging.getLogger("Phenomena")

# EPSG:2085 - Cuba Norte 
# CUBAN_PJ = pj.Proj(proj="lcc", lat_1=22.35, lat_0=22.35, lon_0=-81, k_0=0.99993602,\
#                x_0=500000, y_0=280296.016, ellps="clrk66", datum="NAD27", units="m")

class Phenomena:
    def __init__(self,ipos,jpos,gp):
        self.gp = gp
        self.ipos = ipos*250
        self.jpos = jpos*250

        try:
            self.DB_CONN = gp.DB_CONN
        except:
            logger.error("Cannot connect to database")
            
        self.data = gp.data
        self.adata = gp.adata
            
        # u = ipos*250 # m
        # v = jpos*250 # m
        
        # proj_p = gp.radar_pj(u,v,inverse = True )
        # self.longitude = proj_p[0]
        # self.latitude = proj_p[1]
#         print("'lon':%.4f, 'lat':%.4f" % (proj_p[0],proj_p[1]))

        # proj_p = CUBAN_PJ(proj_p[0], proj_p[1])
        #
        # self.point = "%.4f %.4f" % (proj_p[0],proj_p[1])
        self.line_past = []
        self.line_forecast = []
        
        
    def set_line_past(self,line):
        self.line_past = line
        
        
    def set_line_forecast(self,line):
        self.line_forecast = line

    #
    #
    # def checkLines(self):
    #     if (self.line_past == ""):
    #         self.line_past = "%s,%s" % (self.point, self.point)
    #     if (self.line_forecast == ""):
    #         self.line_forecast = "%s,%s" % (self.point, self.point)
            
            
    def commit(self):
        pass
        