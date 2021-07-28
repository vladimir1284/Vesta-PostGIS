'''
Created on 11/04/2013

@author: vladimir
'''

from Binary_Packages import read_half
from Phenomenon.StromCell import StormCell
import logging

logger = logging.getLogger("Package_15")

class Package_15:
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
        logger.debug("Packet 15: Storm ID Data")

        length=read_half(binaryfile) # length in bytes 

        num=length/6
  
        logger.debug("Packet 15: Length=%4hd  Number Included=%hd" % (length,num))
               

        if (length == 6): # only one symbol
            ipos=read_half(binaryfile)
            jpos=read_half(binaryfile)
            cell_id = binaryfile.read(2).decode("utf-8") 
            
            logger.debug("  I Pos: %4hd  J Pos: %4hd  Storm ID: %s\n" % 
                         (ipos,jpos,cell_id))
        else:
            logger.warning("More than one symbol in packet. Not handled.")
            
        if gp.pdb.MH_msg_code == 58:
            try:
                if not(gp.storm.commited):
                    gp.storm.commit()
            except:
                pass
            gp.storm = StormCell(ipos, jpos, cell_id, gp)
            
        if gp.pdb.MH_msg_code == 59:
            gp.hail.set_id(cell_id, ipos, jpos)
            
        if gp.pdb.MH_msg_code == 61:
            gp.tornado.set_id(cell_id)
            