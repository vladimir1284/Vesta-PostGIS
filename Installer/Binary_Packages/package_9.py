'''
Created on 16/04/2013

@author: vladimir
'''
from Binary_Packages.Package import Package
from Binary_Packages import read_half
import logging
import pylab

logger = logging.getLogger("Package_9")

class Package_9(Package):
    '''
    Figure 3-7 Linked Vector Packet - Packet Code 9 (Sheet 2)
    page 3-86. Document Number 2620001L
    '''
 
    def __init__(self, gp):
        '''
        Constructor
        '''

        self.length = read_half(gp.binaryfile)
        self.color  = read_half(gp.binaryfile)
        
        self.i_start = read_half(gp.binaryfile)
        self.j_start = read_half(gp.binaryfile)
        
        self.length -= 4 # account for the starting points 
        num_vectors = self.length/4
        
        self.i_ends = []
        self.j_ends = []
        
        for i in xrange(num_vectors):
            self.i_ends.append(read_half(gp.binaryfile))
            self.j_ends.append(read_half(gp.binaryfile))
        
        self.i_ends.insert(0, self.i_start)
        self.j_ends.insert(0, self.j_start)
        
    def plot(self,axes, plt):
        axes.plot(self.i_ends,self.j_ends, color = plt.color(self.color))
  
        