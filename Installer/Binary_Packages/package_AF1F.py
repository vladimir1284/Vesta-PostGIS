'''
Created on 31/03/2013

@author: vladimir
'''
from Package import * #@UnusedWildImport
import numpy as np
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

        radial_count          = halves[5]
        
        self.radials = []
        
        for i in xrange(radial_count):
            halves = struct.unpack('>3h',binaryfile.read(6))
            num_rle_halfwords   = halves[0] # Two bytes count
            if (i==0):
                start_angle = halves[1]
                delta_angle = halves[2]
                
                # Angulo central en grados 
                self.ini_angle = (start_angle+delta_angle/2.)/10.
                
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
                radial = np.concatenate((radial,val*np.ones(run)))
                
            self.radials.append(radial)
    
    def writeData(self, band):       
        polar_data = np.array(self.radials, dtype=np.uint8)
        limit = (1e3 * self.gp.pp.range  - self.gp.pp.resolution) / 2.0
        x = y = np.arange(-limit, limit+1, self.gp.pp.resolution)
        cart_data  = polar_to_cart(polar_data, self.ini_angle, 1, self.gp.pp.resolution, x, y)
        band.WriteArray(cart_data)        
