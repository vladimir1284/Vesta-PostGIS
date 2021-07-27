'''
Created on 8 jun. 2021

@author: vladimir
'''
from math import log2
import numpy as np

class VestaColorTable(): 
    def __init__(self, pallete):
        # Load aplletye from file
        fichero = open(pallete,'r')
        try:            
            length = int(fichero.readline())
            self.bitdepth = int(log2(length))
            red = [int(x) for x in fichero.readline().split()]
            green = [int(x) for x in fichero.readline().split()]
            blue = [int(x) for x in fichero.readline().split()]
            # Configure pallete
            self.palette = [(0,0,0,0)]
            for i in range(1,length):
                self.palette.append((red[i], green[i], blue[i], 255))
            self.palette = np.array(self.palette).astype(np.uint8).flatten()
        except:
            print('Error leyendo la paleta')
        
        fichero.close()
    