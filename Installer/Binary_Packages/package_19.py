'''
Created on 11/04/2013

@author: vladimir
'''

from Binary_Packages import read_half
from Phenomenon.Hail import Hail
import logging

logger = logging.getLogger("Package_19")

class Package_19:
    '''
    Figure 3-14. Special Graphic Symbol Packet - Packet Codes 15,
    19, 23, 24 and 25 (Sheet 2)
    page 3-114. Document Number 2620001L
    '''
        
    def __init__(self, gp):
        '''
        Constructor
        '''
        binaryfile = gp.binaryfile
        
        length = read_half(binaryfile)
        logger.debug("Packet 19: HDA Hail Data")
        logger.debug("Value of -999 indicates that the cell is beyond the maximum")
        logger.debug("  range for algorithm processing")
        
        num = length/10
        logger.debug("Length of Data Block (in bytes) = %hd Number included=%d" 
                     % (length,num))
        
        if (length == 10): # only one symbol
            ipos=read_half(binaryfile)
            jpos=read_half(binaryfile)
            prob=read_half(binaryfile)
            prob_sevr=read_half(binaryfile)
            m_size=read_half(binaryfile)
            
            logger.debug("""  I Pos: %4hd  J Pos: %4hd  Prob of Hail: %hd
                    \t\t\t\t\t\t of Severe Hail: %hd  Max Size (in): %hd""" %
                         (ipos,jpos,prob,prob_sevr,m_size))
            
            if (prob!=-999)&(prob_sevr!=-999):
                if (prob!=0)or(prob_sevr!=0):
                    gp.hail = Hail(ipos,jpos,prob,prob_sevr,m_size,gp)
        else:
            logger.warning("More than one symbol in packet. Not handled.")
            