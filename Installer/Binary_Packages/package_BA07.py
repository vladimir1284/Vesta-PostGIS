'''
Created on 31/03/2013

@author: vladimir
'''
from Binary_Packages import read_half, np
import struct
import logging

logger = logging.getLogger("Package_BA07")


class Package_BA07:
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
        
        halves = struct.unpack('>10h', binaryfile.read(20))
        
        num_rows = halves[8]

        self.rows = []
        for i in range(num_rows):
            # read the row header    
            num_bytes = read_half(binaryfile)

            s = binaryfile.read(num_bytes)
            data = struct.unpack(str(num_bytes) + 'B', s)
 
            row = []
            for j in range(num_bytes):
                c = data[j]
                run = c >> 4  # Amount of cells
                val = c & 0xf  # Value of cells  
                print(run, val)           
                # for k in range(run): row.append(val)
                # should be more efficient concatenate
                row = np.concatenate((row, val * np.ones(run)))
                
            self.rows.append(row)
            
        
        
    def writeData(self):       
        return np.array(self.rows, dtype=np.uint8)

