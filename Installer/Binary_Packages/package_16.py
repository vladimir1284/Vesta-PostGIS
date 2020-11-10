'''
Created on 09/04/2013

@author: vladimir
'''

import struct
import pylab
from Package import *
from matplotlib import colors
import logging

logger = logging.getLogger("Package_16")

class Package_16(Package):
    '''
    Figure 3-14. Special Graphic Symbol Packet - Packet Code 26 (Sheet 3)
    page 3-115. Document Number 2620001L
    '''
    def __init__(self, gp):
        '''
        Constructor
        '''
        self.gp = gp
               
        ppi = struct.unpack('>6H',gp.binaryfile.read(12))
#        index_first_range_bin   = ppi[0]
        self.range_bin_count         = ppi[1]
#        i_center                = ppi[2]
#        j_center                = ppi[3]
#        scaled_factor           = ppi[4]
        radial_count            = ppi[5]
        
        self.radials = []
        self.angles = []
        self.ranges = pylab.linspace(0, self.range_bin_count, 
                                     self.range_bin_count)
        self.elevation = gp.pdb.param_3/10. # Elevation angle in degree
        
        for i in xrange(radial_count):
            sector = struct.unpack('>3H',gp.binaryfile.read(6))
            num_bytes = sector[0]
            start_angle = sector[1]
            delta_angle = sector[2]
            
            # Angulo central en grados 
            angle = (start_angle+delta_angle/2.)/10. 
            
            # Convertido a radianes, rotado e invertido el sentido            
            self.angles.append((90-angle)*pylab.pi/180) 

            self.radials.append(struct.unpack(str(num_bytes)+'B',
                                gp.binaryfile.read(num_bytes)))
            
        gp.georeference.append(self.getlimits())
        
        
    
    def getlimits(self):
        istart = 0#JCoorStart*250 # m
        jstart = 0#ICoorStart*250 # m
        theta = pylab.pi*(self.elevation)/180
        
        space = self.gp.pp.resolution
        space = RE*pylab.arcsin(space*pylab.cos(theta)/pylab.sqrt(RE**2+2*space*RE*pylab.sin(theta)+space**2))
        xmax = self.range_bin_count*space + istart
        ymax = self.range_bin_count*space + jstart
        xmin = -self.range_bin_count*space + istart
        ymin = -self.range_bin_count*space + jstart
        
        proj_p_max = self.gp.radar_pj(xmax,ymax,inverse = True)
        proj_p_min = self.gp.radar_pj(xmin,ymin,inverse = True)
        
        proj_p_max = CUBAN_PJ(proj_p_max[0],proj_p_max[1])
        proj_p_min = CUBAN_PJ(proj_p_min[0],proj_p_min[1])
        
        self.xmax = proj_p_max[0]
        self.ymax = proj_p_max[1]
        self.xmin = proj_p_min[0]
        self.ymin = proj_p_min[1]
        
        return [self.xmin, self.ymin, self.xmax, self.ymax]
    
    
    def plot(self,axes, plt):
        #rectangular plot of polar data
        rad, theta = pylab.meshgrid(self.ranges, self.angles) 
        X = theta
        Y = rad
        norm = colors.Normalize(vmin = 1, vmax = plt.length-1, clip = False)
        axes.pcolormesh(X, Y, pylab.array(self.radials), cmap = plt.cm, 
                        norm = norm)            
            
