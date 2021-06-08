'''
Created on 12/04/2013

@author: vladimir
'''
from Binary_Packages import read_half
from Phenomenon.Tornado import Tornado
import logging

logger = logging.getLogger("Package_12")

class Package_12:
    '''
    Figure 3-14. Special Graphic Symbol Packet - Packet Code 3 
    or 11, 12 or 26, 13 and 14(Sheet 1)
    page 3-113. Document Number 2620001L
    '''
    
    def __init__(self, gp):
        '''
        Constructor
        '''
        binaryfile = gp.binaryfile
        self.length=read_half(binaryfile)
        
#         if DEBUG:
#             print "Packet 12: Tornado Vortex Signature"
# 
        self.num=self.length/4;
        if self.num != 1:
            logger.warning("More than one symbol in packet. Not handled.")
#     
#             print "TVS Block Length %hd  Number Included %hd\n" %(self.length,self.num)
#     
#              in this packet there are 2 fields (4 bytes) to be 
#              written for each symbol 
#     
#             for i in xrange(self.num):      
#                 self.ipos=read_half(binaryfile)
#                 self.jpos=read_half(binaryfile)
#                 print "  I Pos: %4hd  J Pos: %4hd\n" %(self.ipos,self.jpos);
#         else:
        self.ipos=read_half(binaryfile)
        self.jpos=read_half(binaryfile)
        gp.tornado = Tornado(self.ipos, self.jpos, False, gp)
        
        logger.debug("Packet 12: Tornado Vortex Signature")
        logger.debug("TVS Block Length %hd  Number Included %hd" %
                     (self.length,self.num))
        logger.debug("  I Pos: %4hd  J Pos: %4hd" %(self.ipos,self.jpos))
