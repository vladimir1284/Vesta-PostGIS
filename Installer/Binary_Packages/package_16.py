'''
Created on 31/03/2013

@author: vladimir
'''
from Package import * #@UnusedWildImport
import numpy as np
import logging

logger = logging.getLogger("Package_AF1F")

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
        binaryfile = gp.binaryfile
        
        halves = struct.unpack('>6h',binaryfile.read(12))

        radial_count = halves[5]
        
        self.radials = []
        
        for i in xrange(radial_count):
            sector = struct.unpack('>3H',gp.binaryfile.read(6))
            num_bytes = sector[0]
            if (i==0):
                start_angle = sector[1]
                delta_angle = sector[2]
                
                # Angulo central en grados 
                self.ini_angle = (start_angle+delta_angle/2.)/10. 

            self.radials.append(struct.unpack(str(num_bytes)+'B',
                                gp.binaryfile.read(num_bytes)))
            
    
    def writeData(self, band):       
        polar_data = np.array(self.radials, dtype=np.uint8)
        limit = (1e3 * self.gp.pp.range  - self.gp.pp.resolution) / 2.0
        x = y = np.arange(-limit, limit+1, self.gp.pp.resolution)
        cart_data  = polar_to_cart(polar_data, self.ini_angle, 1, self.gp.pp.resolution, x, y)
        band.WriteArray(cart_data)        
