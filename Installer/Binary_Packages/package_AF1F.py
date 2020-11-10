'''
Created on 31/03/2013

@author: vladimir
'''
from Package import * #@UnusedWildImport
import pylab
from matplotlib import colors
import logging

logger = logging.getLogger("Package_AF1F")

class Package_AF1F(Package):
    '''
    Figure 3-10. Radial Data Packet (16 Data Levels) - Packet Code AF1F (Sheet 1-2)
    page 3-103. Document Number 2620001L
    '''


    def __init__(self, gp):
        '''
        Constructor
        '''
        self.gp = gp
        binaryfile = gp.binaryfile
        
        halves = struct.unpack('>6h',binaryfile.read(12))
#        index_first_range_bin = halves[0]
        self.range_bin_count  = halves[1]
#         i_center              = halves[2]
#         j_center              = halves[3]
#        scaled_factor         = halves[4]
        radial_count          = halves[5]
        
        self.radials = []
        self.angles = []
        self.ranges = pylab.linspace(0, self.range_bin_count, 
                                  self.range_bin_count)
        self.elevation = gp.pdb.param_3/10. # Elevation angle in degree
        
        for i in xrange(radial_count):
            halves = struct.unpack('>3h',binaryfile.read(6))
            num_rle_halfwords   = halves[0] # Two bytes count
            start_angle         = halves[1]           
            delta_angle         = halves[2]
            
            angle = (start_angle+delta_angle/2.)/10. # Central angle in degres
          
            self.angles.append((90-angle)*pylab.pi/180) # Radians, rotated and inverted rotation

            num_bytes = 2*num_rle_halfwords
            radial = []
            s = binaryfile.read(num_bytes)
            data = struct.unpack(str(num_bytes)+'B',s)
 
            radial = []
            for j in xrange(num_bytes):
                c = data[j]
                run = c/16 # Cantidad de celdas
                val = c&0xf # Valor de las celdas               
                #for k in xrange(run): radial.append(val)
                # should be more efficient concatenate
                radial = pylab.concatenate((radial,val*pylab.ones(run)))
                
            self.radials.append(radial)
            
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
        rad, theta = pylab.meshgrid(self.ranges, self.angles) #rectangular plot of polar data
        X = theta
        Y = rad
        norm = colors.Normalize(vmin = 1, vmax = plt.length-1, clip = False)
        axes.pcolormesh(X, Y, pylab.array(self.radials), cmap = plt.cm, norm = norm)
