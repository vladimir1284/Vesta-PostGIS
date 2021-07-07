'''
Created on 12/04/2013

@author: vladimir
'''
from Binary_Packages import read_half
from Binary_Packages.Package import CUBAN_PJ, Package
import logging

logger = logging.getLogger("Package_6")

class Package_6(Package):
    '''
    Figure 3-7 Linked Vector Packet - Packet Code 6 (Sheet 1)
    page 3-86. Document Number 2620001L
    '''    
    
    def __init__(self, gp, set_line=None):
        '''
        Constructor
        '''
        
        binaryfile = gp.binaryfile
        
        length = read_half(binaryfile)
        num_vectors=length/4;
        
        logger.debug("Packet 6: Linked Vector Packet (no value)")
        logger.debug("Packet 6 Length of Data Block (in bytes) = %hd" % length)
        logger.debug("Number of Vectors: %i" % num_vectors)        
        
        tmp = []            
        for i in xrange(0,length,4):
            u = read_half(binaryfile)
            v = read_half(binaryfile)
            logger.debug("  I Starting Point: %hd   J Starting Point: %hd" % (u,v))
            u *= 250 # m
            v *= 250 # m
            tmp.append([u, v])
            
        if set_line != None:
            set_line(tmp)
            
        logger.debug("Packet 6 Complete")
