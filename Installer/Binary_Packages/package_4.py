'''
Created on 16/04/2013

@author: vladimir
'''

from Binary_Packages import read_half
import logging
import pylab
from Palette import Palette

logger = logging.getLogger("Package_4")

class Package_4:
    '''
    Figure 3-13. Wind Barb Data Packet - Packet Code 4
    page 3-112. Document Number 2620001L
    '''
    plt = Palette('palettes/wind_5.plt')
    def __init__(self, gp):
        '''
        Constructor
        '''
        self.length = read_half(gp.binaryfile)
        self.color_level = read_half(gp.binaryfile)

        if(self.color_level<1) | (self.color_level>5):
            logger.error("Data Error: Color level of %hd was out of range",
                         self.color_level)
    
        self.x=read_half(gp.binaryfile)
        self.y=read_half(gp.binaryfile)
        self.dir=read_half(gp.binaryfile)
        self.spd=read_half(gp.binaryfile)
        
        self.u = self.spd*pylab.sin(pylab.pi/180*(self.dir-180))
        self.v = self.spd*pylab.cos(pylab.pi/180*(self.dir-180))
        
        logger.debug(
        "Packet 4: Length=%4i Barb Color=%3i X Pos: %4i Y Pos: %4i Dir: %3i Speed: %3i" 
                     % (self.length,self.color_level,self.x,self.y,self.dir,self.spd))
    
    def plot(self, axes, plt):
        axes.barbs(self.x, self.y, self.u, self.v, 
                   color = self.plt.color(self.color_level), 
                   length = 6, linewidth = 0.5)
