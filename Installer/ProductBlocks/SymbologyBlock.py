'''
Created on 08/04/2013

@author: vladimir
'''
from bz2 import BZ2Decompressor
from StringIO import StringIO
import struct
import matplotlib
matplotlib.use('Agg')
from ProductBlocks import read_half_unsigned
from SiteConfiguration import OFFSET
import logging
import pylab


from Palette import Palette

from Binary_Packages.package_AF1F   import Package_AF1F
from Binary_Packages.package_BA07   import Package_BA07
from Binary_Packages.package_16     import Package_16
from Binary_Packages.package_19     import Package_19
from Binary_Packages.package_15     import Package_15
from Binary_Packages.package_12     import Package_12
from Binary_Packages.package_20     import Package_20
from Binary_Packages.package_10     import Package_10
from Binary_Packages.package_8      import Package_8
from Binary_Packages.package_4      import Package_4
from Binary_Packages.package_9      import Package_9
from Binary_Packages.package_23     import Package_23
from Binary_Packages.package_24     import Package_24
from Binary_Packages.package_2      import Package_2


PACKAGES = {0xba07: Package_BA07, 0xaf1f:Package_AF1F, 16: Package_16,
            19: Package_19, 15: Package_15, 12: Package_12, 20: Package_20,
            8: Package_8, 23: Package_23, 2: Package_2, 10: Package_10,
            9: Package_9, 4: Package_4, 24: Package_24}

logger = logging.getLogger("SymbologyBlock")

class SymbologyBlock:
    '''
    classdocs
    '''


    def __init__(self, gp):
        '''
        Constructor
        '''    
	self.gp = gp
        gp.binaryfile.seek(OFFSET + gp.pdb.sym_off*2,0)
        #pcode = gp.pdb.MH_msg_code
        
        # Check for compressed Symbology Block
        if gp.pp.compressed:
            decompressor = BZ2Decompressor()
            symb_string = decompressor.decompress(gp.binaryfile.read())
            gp.binaryfile = StringIO(symb_string) # Handle string as file         

        blockHeader = struct.unpack('>hHiH',gp.binaryfile.read(10))
        self.divider    = blockHeader[0]    # value of -1 used to delineate the following from 
                                            # the above product description block; DIV2OFF 61
        self.block_id  = blockHeader[1]     # always 1 
        self.block_len = blockHeader[2]     # length of this block in bytes including the 
                                            # preceding devider and block id; 1 - 80000 
        self.n_layers   = blockHeader[3]    # number of data layers obtained in this block; 
                                            # 1 - 15     
        
        
        #for i in xrange(self.n_layers):
        layerHeader = struct.unpack('>hi',gp.binaryfile.read(6))  
        layer_divider = layerHeader[0]  # value of -1 used to delineate one data layer 
                                        # from another 
        self.data_len = layerHeader[1]  # length of data layer (in bytes) starting from the 
                                        # bytes after this int and ending at the last data
                                        # of this layer; 1 - 80000*/
          
            
        actual_position = gp.binaryfile.tell()       
        end_position = self.data_len + actual_position
        
        if gp.pp.non_graphic:
#            #context.gp.msg_code in NON_GRAPHIC:
#            #context.fig = figure(figsize=(5.974,5.974))
#            fig = matplotlib.figure(figsize=(15,15))
#            #context.dbname = TABLE[context.gp.msg_code]
#            #context.msg_Track_inf = Tracking_information(context)
#            #context.msg_59 = Hail(context)
            while (actual_position < end_position):
                packet_code = read_half_unsigned(gp.binaryfile)
                package = PACKAGES[packet_code](gp)
                actual_position = gp.binaryfile.tell()
                
            # Check for last phenomena commit
            if gp.pdb.MH_msg_code == 141:
                if not(gp.mesocyclone.commited):
                    gp.mesocyclone.commit()
                    
            if gp.pdb.MH_msg_code == 58:
                if not(gp.storm.commited):
                    gp.storm.commit()
                    
        else:
            if gp.pp.geographic:
                figureSize = (6,6)
            else:
                figureSize = (8,8) # Bigger for VAD & VWP
                # Update DB
                query_str = """SELECT insert_graphic_product
                    ('%s','%s',%i,'%s','%s','%s');""" % (gp.datetime,
                    gp.RADAR_ID, gp.pdb.MH_msg_code, 
                    gp.dirname + '/' + gp.file_name, gp.data, gp.adata)
                logger.debug(query_str)
                try:      
                    gp.DB_CONN.query(query_str)
                except:
                    logger.error(self.DB_CONN.error)
                    
            fig = pylab.figure(figsize=figureSize)
            
            ax = pylab.axes(axisbg = 'w', polar=gp.pp.polar)
            plt = Palette('palettes/'+gp.pp.palette)
            
            # Repeat for each package in the layer
            while (actual_position < end_position):
                packet_code = read_half_unsigned(gp.binaryfile)
                package = PACKAGES[packet_code](gp)                
                package.plot(ax, plt)
                actual_position = gp.binaryfile.tell()    
                            
            pylab.xticks([])
            pylab.yticks([])
            pylab.axis(gp.pp.axis)
            if gp.pp.polar: 
                pylab.axis('off')
            fig.savefig('images/'+self.gp.RADAR_ID+'/'+gp.file_name, format='png',bbox_inches = 'tight',
                        pad_inches = 0,transparent=gp.pp.transparent)

	    if gp.pp.geographic:
		wfile = file('images/'+self.gp.RADAR_ID+'/'+gp.file_name+'w','w')
            	wfile.write(self.georeference())
            	wfile.close()

            gp.images.append(gp.file_name)


    def georeference(self):     
        Npixels = 465 # This is a gospel truth
        [minx, miny, maxx, maxy] = self.gp.georeference[0]
        del_x  = (maxx - minx)/(Npixels-1)
        del_y  = (maxy - miny)/(Npixels-1)
        x_left = minx
        y_up   = maxy
        return "%.2f\n0.0000000000\n0.0000000000\n-%.2f\n%.2f\n%.2f" %\
                (del_x, del_y, x_left, y_up) 
