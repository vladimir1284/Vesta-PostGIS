'''
Created on 31/03/2013

@author: vladimir
'''
from Package import * #@UnusedWildImport
from Binary_Packages import read_half

import pylab
from matplotlib import colors
import logging

logger = logging.getLogger("Package_BA07")

class Package_BA07(Package):
    '''
    Figure 3-11. Raster Data Packet - Packet Codes BA0F and BA07 (Sheet 1-2)
    page 3-105. Document Number 2620001L
    '''


    def __init__(self, gp):
        '''
        Constructor
        '''
        
        binaryfile = gp.binaryfile
        self.gp = gp
        
        halves = struct.unpack('>10h',binaryfile.read(20))
        
#        packType            = halves[0]
#        packType1           = halves[1]
#        ICoorStart          = halves[2]
#        JCoorStart          = halves[3]
#        XScale              = halves[4]
#        XScaleFract         = halves[5]
#        YScale              = halves[6]
#        YScaleFract         = halves[7]
        self.num_rows       = halves[8]
#        packingDescriptor   = halves[9]

        self.rows = []
        for i in xrange(self.num_rows):
            # read the row header    
            num_bytes = read_half(binaryfile)

            s = binaryfile.read(num_bytes)
            data = struct.unpack(str(num_bytes)+'B',s)
 
            row = []
            for j in xrange(num_bytes):
                c = data[j]
                run = c/16  # Amount of cells
                val = c&0xf # Value of cells             
                #for k in xrange(run): row.append(val)
                # should be more efficient concatenate
                row = pylab.concatenate((row,val*pylab.ones(run)))
                
            self.rows.append(row)
            
        self.num_cols = len(row) # Amount of columns
        
        gp.georeference.append(self.getlimits())
    
    def getlimits(self):
        istart = 0#ICoorStart*250 # m
        jstart = 0#JCoorStart*250 # m
        XScale = self.gp.pp.resolution
        YScale = XScale
        xmax = self.num_cols*XScale/2. + istart
        ymax = self.num_rows*YScale/2. + jstart
        xmin = -self.num_cols*XScale/2. + istart
        ymin = -self.num_rows*YScale/2 + jstart
        
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
        norm = colors.Normalize(vmin = 1, vmax = plt.length-1, clip = False)        
        axes.imshow(self.rows, interpolation = 'nearest', norm = norm, cmap = plt.cm)
