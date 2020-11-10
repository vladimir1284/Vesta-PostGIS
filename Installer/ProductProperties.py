'''
Created on 08/04/2013

@author: vladimir
'''
from xml.dom import minidom

AXIS = {0:[-1,513,513,-1],
        1:'off',
        2:[0,0,0,230],
        3:True,
        4:[0,0,0,920],
        5:[0,1000,513,0],
        6:[0,0,0,460]}
    
class ProductProperties:
    '''
    Read and process product properties from XML file
    '''    
    def __init__(self, filename, pcode):
        '''
        Constructor
        '''
        self.product_table = minidom.parse(filename)
        self.pcode = pcode
        productNode = self.getProductNode()
        
        self.resolution = 1e3*float(productNode.attributes['resolution'].value)
        self.polar = self.tf(productNode.attributes['polar'].value)
        self.compressed = self.tf(productNode.attributes['compressed'].value)
        self.name = productNode.attributes['name'].value
        self.mosaic_name = productNode.attributes['mosaic_name'].value
        self.palette = productNode.attributes['palette'].value
        self.transparent = self.tf(productNode.attributes['transparent'].value)
        self.axis = AXIS[int(productNode.attributes['axis'].value)]
        self.stand_alone = self.tf(productNode.attributes['stand_alone'].value)
        self.non_graphic = self.tf(productNode.attributes['non_graphic'].value)
        self.geographic = self.tf(productNode.attributes['geographic'].value)
        self.range = int(productNode.attributes['range'].value)
        
        
    def tf(self,text):
        result = None
        if text == "True":
            result = True
        if text == "False":
            result = False
            
        if result == None:
            class WrongBoolean_Exception(BaseException):
                pass
            raise WrongBoolean_Exception('The word \"%s\" should be True or False!!!' % text)
        return result    
    
    
    def getProductNode(self):
        result = None
        Nodes = self.product_table.getElementsByTagName('product')
        for node in Nodes:
            if int(node.attributes['pcode'].value) == self.pcode:
                result = node
        if result == None:
            class NoProduct_Exception(BaseException):
                pass
            raise NoProduct_Exception('No product with pcode = %i defined on XML file.' % self.pcode)
        return result
    
    
    def getProperties(self):
        return '\n========= Product Properties ========\n' +\
        'Pcode: '+str(self.pcode)+'\n'+\
        'Resolution: '+str(self.resolution)+'m\n'+\
        'Range: '+str(self.range)+'km\n'+\
        'Polar: '+str(self.polar)+'\n'+\
        'Compressed: '+str(self.compressed)+'\n'+\
        'Name: '+str(self.name)+'\n'+\
        'Mosaic Name: '+str(self.mosaic_name)+'\n'+\
        'Palette file name: '+str(self.palette)+'\n'+\
        'Transparent: '+str(self.transparent)+'\n'+\
        'Axis: '+str(self.axis)+'\n'+\
        'Stand-Alone Tabular Alphanumeric Product Message: '+str(self.stand_alone)+\
        '\nNon graphic product: '+str(self.non_graphic)+'\n'\
        'Geographic product: '+str(self.geographic)+'\n'