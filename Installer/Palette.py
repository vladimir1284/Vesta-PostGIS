'''
Created on 08/04/2013

@author: vladimir
'''
from matplotlib.colors import ListedColormap

class Palette:
    def __init__(self,file_name):
        fichero = file(file_name,'r')
        try:            
            self.length = int(fichero.readline())
            #self.dic = {}
            self.red = [int(x) for x in fichero.readline().split()]
            self.green = [int(x) for x in fichero.readline().split()]
            self.blue = [int(x) for x in fichero.readline().split()]
            sec = []
            for i in xrange(1,self.length):
                sec.append((self.red[i]/255., self.green[i]/255., self.blue[i]/255.))
                #self.dic[i] = [self.red[i]/255., self.green[i]/255., self.blue[i]/255.]
            self.cm = ListedColormap(sec)
            self.cm.set_under(color='k', alpha=0)
        except:
            print 'Error leyendo la paleta'
        
        fichero.close()
    
    def color(self, value):
        if value>=self.length:
            print 'Valor de color fuera de rango'
        rgb = (self.red[value]/255., self.green[value]/255., self.blue[value]/255.)
        return rgb
