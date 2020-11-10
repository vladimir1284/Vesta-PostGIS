'''
Created on 12/04/2013

@author: vladimir
'''
from Package import Package
from Binary_Packages import read_half
from Phenomenon.Mesocyclone import Mesocyclone
import logging

logger = logging.getLogger("Package_20")

class Package_20(Package):
    '''
    Figure 3-14. Special Graphic Symbol Packet - Packet Code 20 (Sheet 4)
    page 3-116. Document Number 2620001L
    '''
 
    def __init__(self, gp):
        '''
        Constructor
        '''        
        length=read_half(gp.binaryfile)
        num=length/8 
        
        # in this packet there are 4 fields (8 bytes) to be 
        # written for each symbol        
        for i in xrange(num):
            ipos=read_half(gp.binaryfile)
            jpos=read_half(gp.binaryfile)
            FeatureType=read_half(gp.binaryfile)
            attribute=read_half(gp.binaryfile)
            
            logger.debug("Packet 20: Generic Point Feature")
            logger.debug("Packet 20: Length=%4hd  Number Included=%hd" % (length,num))                
            logger.debug("""  I Pos: %4hd  J Pos: %4hd  Feature Type: %hd                              
                                             Attribute: %hd""" % \
                        (ipos,jpos,FeatureType,attribute))
            
        if gp.pdb.MH_msg_code != 141:
            logger.warning("This package is intended for product 141 by now!!!")

        gp.mesocyclone = Mesocyclone(ipos, jpos, FeatureType, attribute, gp)
