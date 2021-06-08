'''
Created on 16/04/2013

@author: vladimir
'''
from Package import Package
from Binary_Packages import read_half
from Binary_Packages.package_6 import Package_6
import logging

logger = logging.getLogger("Package_24")

class Package_24(Package):
    '''
    Figure 3-14. Special Graphic Symbol Packet - Packet Codes 15, 
    19, 23, 24 and 25 (Sheet 2)
    page 3-114. Document Number 2620001L
    '''
 
    def __init__(self, gp):
        """
        Constructor
        """
        
        binaryfile = gp.binaryfile
        
        length = read_half(binaryfile)
        actual_position = binaryfile.tell()
        p_end_offset = actual_position+length-2
        
        logger.debug("Packet 24: SCIT Forecast Position Data")
        logger.debug("Length of Data Block (in bytes) = %hd" % length)
           
        while (actual_position < p_end_offset):
            p_packet_code = read_half(binaryfile)
            if (p_packet_code == 6): # TODO also posible 2 or 25
                if gp.pdb.MH_msg_code == 141:
                    package = Package_6(gp, gp.mesocyclone.set_line_forecast)
                if gp.pdb.MH_msg_code == 58:
                    package = Package_6(gp, gp.storm.set_line_forecast)
            else:
                binaryfile.seek(read_half(binaryfile),1)      
                logger.warning("Packet code %i not handled yet!!!" % p_packet_code) 
                          
            actual_position = binaryfile.tell()
