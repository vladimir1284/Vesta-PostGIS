'''
Created on 16/04/2013

@author: vladimir
'''
from Binary_Packages.Package import Package
from Binary_Packages import read_half
import logging
import pylab

logger = logging.getLogger("Package_10")

class Package_10(Package):
    '''
    Figure 3-8. Unlinked Vector Packet - Packet Code 10 (Sheet 2)
    page 3-89. Document Number 2620001L
    '''
 
    def __init__(self, gp):
        '''
        Constructor
        '''
        
        self.binaryfile = gp.binaryfile
        self.length=read_half(self.binaryfile)
        self.color=read_half(self.binaryfile)
        
        if(self.color<1) | (self.color>16):
            logger.error("Data Error: Color level was out of range")
            
        self.length -= 2 # account for the color&length values
        self.num_vectors=self.length/8
        

    def plot(self, axes, plt):
        logger.debug('Color Level: %i' % self.color)
        cl = plt.color(self.color)
        for i in xrange(self.num_vectors):
            begI=read_half(self.binaryfile)
            begJ=read_half(self.binaryfile)
            endI=read_half(self.binaryfile)
            endJ=read_half(self.binaryfile)
            logger.debug('Vector: %i\tbegI: %3i\tbegJ: %3i\tendI: %3i\tendJ: %3i' % 
                         (i+1, begI, begJ, endI, endJ))
            l = pylab.Line2D([begI,endI], [begJ,endJ], color = cl)                                    
            axes.add_line(l) 

