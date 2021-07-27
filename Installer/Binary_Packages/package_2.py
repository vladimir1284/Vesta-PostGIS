'''
Created on 13/04/2013

@author: vladimir
'''

from Binary_Packages import read_half
import logging

logger = logging.getLogger("Package_2")

class Package_2:
    """
    Figure 3-8b. Text and Special Symbol Packets - Packet Code 2 (Sheet 3)
    page 3-97. Document Number 2620001L
    """
    def __init__(self, gp):
        '''
        Constructor
        '''
        
        binaryfile = gp.binaryfile
        
        length=read_half(binaryfile)
        
        logger.debug("Packet 2: Write Special Symbols (No Value) Summary Information")            
        logger.debug("Length of Data Block (in bytes) = %i" % length)
        i = read_half(binaryfile)
        j = read_half(binaryfile)
        logger.debug("I Starting Point: %i" % i)
        logger.debug("J Starting Point: %i" % j)

        length-=4;
 
        logger.debug("Message Begins at next line:")

        logger.debug(binaryfile.read(length))
        logger.debug("Message Complete\n")
#         else:
#             binaryfile.seek(length,1)
            