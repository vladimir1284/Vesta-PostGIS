'''
Created on 12/04/2013

@author: vladimir
'''
from SiteConfiguration import FONT_SIZE
from Binary_Packages import read_half
import logging
from Binary_Packages.Package import Package

logger = logging.getLogger("Package_8")

class Package_8(Package):
    '''
    Figure 3-8b. Text and Special Symbol Packets - Packet Code 8 (Sheet 2)
    page 3-96. Document Number 2620001L
    '''
 
    def __init__(self, gp):
        '''
        Constructor
        '''
        self.length=read_half(gp.binaryfile)

        self.color=read_half(gp.binaryfile)
        self.ipos=read_half(gp.binaryfile)
        self.jpos=read_half(gp.binaryfile)
       
        self.length -= 6 # account for the color/I/J Pos values
        
        self.text = gp.binaryfile.read(self.length) # Leyendo cadena
        

        logger.debug("Packet 8: Length=%4i  Text Color=%3i  I Pos: %4i  J Pos: %4i" 
                  % (self.length,self.color,self.ipos,self.jpos))
        logger.debug("  Text: %s\n" % self.text)
            
        if (gp.pdb.MH_msg_code == 141):
            gp.mesocyclone.set_id(self.text,self.ipos,self.jpos)
        
    def plot(self,axes, plt):
        axes.text(self.ipos, self.jpos+FONT_SIZE, self.text, 
                  fontsize = FONT_SIZE, color = plt.color(self.color),
                  horizontalalignment='left') 

