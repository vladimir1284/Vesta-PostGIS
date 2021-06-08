'''
Created on 8 jun. 2021

@author: vladimir
'''
from gdal import  ColorTable

class VestaColorTable(ColorTable): 
    def __init__(self, pallete):
        # Invoke ColorTable constructor
        ColorTable.__init__(self)
        # Load aplletye from file
        fichero = file(pallete,'r')
        try:            
            length = int(fichero.readline())
            red = [int(x) for x in fichero.readline().split()]
            green = [int(x) for x in fichero.readline().split()]
            blue = [int(x) for x in fichero.readline().split()]
            # Configure pallete
            self.SetColorEntry(0,(0,0,0,0))
            for i in range(1,length):
                self.SetColorEntry(i, (red[i], green[i], blue[i], 255))

        except:
            print 'Error leyendo la paleta'
        
        fichero.close()
    