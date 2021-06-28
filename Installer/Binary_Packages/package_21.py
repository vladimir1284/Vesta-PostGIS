'''
Created on 13/04/2013

@author: vladimir
'''
from Package import Package
import struct, pylab
import logging

logger = logging.getLogger("Package_21")

class Package_21(Package):
    """
    Figure 3-15. Cell Trend Data Packet - Packet Code 21 (Sheet 1)
    page 3-117. Document Number 2620001L
    """
    
#     TREND_CODE_FACTOR = {1:100.,2:100.,3:100.,4:1,5:1,6:1,7:1,8:100.}
    
    def __init__(self, binaryfile):
        '''
        Constructor
        '''
        
        
        cell_id = binaryfile.read(2)
        
        self.cell = Cell_trend(cell_id)
        
        coord = struct.unpack('>2h',binaryfile.read(4))
        Ipos = coord[0] # Cell I coordinate at latest Volume Scan
        Jpos = coord[1] # Cell J coordinate at latest Volume Scan

         
        self.Ipos = Ipos/8
        self.Jpos = Jpos/8
         
        for i in xrange(8):
            trend_header = struct.unpack('>h2b',binaryfile.read(4))
            trend_code = trend_header[0]    # Indicates trend data type to follow:
                                            #    1 = cell top
                                            #    2 = cell base
                                            #    3 = max. ref. hgt.
                                            #    4 = prob. hail
                                            #    5 = prob. svr. hail
                                            #    6 = cell based VIL
                                            #    7 = max. ref.
                                            #    8 = centroid hgt.
            num_vol = trend_header[1]       # Number of volume scans of trend data for
                                            # this trend code in the circular list
            latest_vol_ptr=trend_header[2]  # Pointer to the latest volume scan 
                                            # in the circular list
         
            values = struct.unpack('>'+str(num_vol)+'H',binaryfile.read(2*num_vol))
#             values = [x/self.TREND_CODE_FACTOR[trend_code] for x in values] # 100 Feet
            self.cell.setValues(trend_code, pylab.array(values))


class Cell_trend:
    def __init__(self, cell_id):
        self.TREND_DATA = {1:self.setCell_top, 2:self.setCell_base,
                           3:self.setMax_ref_hgt, 4:self.setProb_hail,
                           5:self.setProb_svr_hail,6:self.setCell_based_VIL,
                           7:self.setMax_ref, 8:self.setCentroid_hgt}
        self.cell_id = cell_id
        
    def setValues(self, trend_code, values):
        self.TREND_DATA[trend_code](values)
        
    def setCell_top(self, values):
        # If the value is over 700, then 1000 has been added to denote that 
        # the CELL TOP (BASE) was detected on the highest (lowest) elevation scan.
#         values = pylab.array(values)
#         values[values > 700] = values[values > 700] - 1000
        self.cell_top = values/10.
        
    def setCell_base(self, values):
        # If the value is over 700, then 1000 has been added to denote that 
        # the CELL TOP (BASE) was detected on the highest (lowest) elevation scan.
#         values = pylab.array(values)
#         values[values > 700] = values[values > 700] - 1000
        self.cell_base = values/10.
        
    def setMax_ref_hgt(self, values):
        self.max_ref_hgt = values/10.
        
        
    def setProb_hail(self, values):
        self.prob_hail = values
        
        
    def setProb_svr_hail(self, values):
        self.prob_svr_hail = values
        
        
    def setCell_based_VIL(self, values):
        self.cell_based_VIL = values
        
        
    def setMax_ref(self, values):
        self.max_ref = values
        
        
    def setCentroid_hgt(self, values):
        self.centroid_hgt = values/10.
        
