'''
Created on 08/04/2013

@author: vladimir
'''
from bz2 import BZ2Decompressor
from io import BytesIO
import struct
import matplotlib
from numpy import matrix
matplotlib.use('Agg')
from ProductBlocks import read_half_unsigned
from SiteConfiguration import OFFSET
import logging
import pylab
import os
import errno
from PIL import Image

'''
        ['lbj';   'pde';   'csb';   'psj';   'cmw';   'pln';   'gpd';   'hlg';   'cnr'   ];
rlon = [-84.4784 -82.5583 -82.3500 -80.1475 -77.8451 -77.4167 -75.6333 -76.2360 -77.8487];
rlat = [ 21.9212  21.5669  23.1495  21.9892  21.3836  19.9167  20.0333  20.9200  21.4233];
ralt = [      15       20       50     1150      160      900     1230      267      150];
'''
RADAR_LOCATIONS =  {'CLBJ':(21.9212, -84.4784),
                    'CPDE':(21.5669, -82.5583),
                    'CCSB':(23.1495, -82.3500),
                    'CPSJ':(21.9892, -80.1475),                   
                    'CPLN':(19.9167, -77.4167),
                    'CGPD':(20.0333, -75.6333),
                    'CHLG':(20.9200, -76.2360),
                    'CCMW':(21.4233, -77.8487)}

from Palette import Palette
from ColorTable import VestaColorTable

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
        gp.binaryfile.seek(OFFSET + gp.pdb.sym_off * 2, 0)
        # pcode = gp.pdb.MH_msg_code
        
        # Check for compressed Symbology Block
        if gp.pp.compressed:
            decompressor = BZ2Decompressor()
            symb_string = decompressor.decompress(gp.binaryfile.read())
            gp.binaryfile = BytesIO(symb_string)  # Handle string as file         

        blockHeader = struct.unpack('>hHiH', gp.binaryfile.read(10))
        self.divider = blockHeader[0]  # value of -1 used to delineate the following from 
                                            # the above product description block; DIV2OFF 61
        self.block_id = blockHeader[1]  # always 1 
        self.block_len = blockHeader[2]  # length of this block in bytes including the 
                                            # preceding devider and block id; 1 - 80000 
        self.n_layers = blockHeader[3]  # number of data layers obtained in this block; 
                                            # 1 - 15     
        
        # for i in range(self.n_layers):
        layerHeader = struct.unpack('>hi', gp.binaryfile.read(6))  
        layer_divider = layerHeader[0]  # value of -1 used to delineate one data layer 
                                        # from another 
        self.data_len = layerHeader[1]  # length of data layer (in bytes) starting from the 
                                        # bytes after this int and ending at the last data
                                        # of this layer; 1 - 80000*/
            
        actual_position = gp.binaryfile.tell()       
        end_position = self.data_len + actual_position
        
        if gp.pp.non_graphic:
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
            # Handle directory creation
            dir_name = 'images/' + self.gp.RADAR_ID + '/'
            if not os.path.exists(os.path.dirname(dir_name)):
                try:
                    os.makedirs(os.path.dirname(dir_name))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            if gp.pp.geographic:                      
                # Repeat for each package in the layer
                while (actual_position < end_position):
                    packet_code = read_half_unsigned(gp.binaryfile)
                    package = PACKAGES[packet_code](gp)            
                    s = package.writeData()   # return image matrix
                    actual_position = gp.binaryfile.tell() 
                    
                # write to disk
                colors = VestaColorTable('palettes/' + gp.pp.palette)
                img = Image.fromarray(s)
                img = img.convert('P')
                img.putpalette(colors.palette, rawmode='RGBA')
                
                self.gp.images.append(gp.file_name +'.png') # For FTP
                img.save(dir_name + gp.file_name +'.png')

            # else:
            #     figureSize = (8, 8)  # Bigger for VAD & VWP
            #     my_dpi = 150.0
            #     # Update DB
            #     query_str = """SELECT insert_graphic_product
            #         ('%s','%s',%i,'%s','%s','%s');""" % (gp.datetime,
            #         gp.RADAR_ID, gp.pdb.MH_msg_code,
            #         gp.dirname + '/' + gp.file_name, gp.data, gp.adata)
            #     logger.debug(query_str)
            #     try: 
            #         gp.DB_CONN.query(query_str)
            #     except:
            #         try:
            #             logger.error(self.DB_CONN.error)
            #         except:
            #             logger.error("There is no database connection")
            #
            #
            #     fig = pylab.figure(figsize=figureSize, dpi=my_dpi)
            #     ax = pylab.Axes(fig, [0., 0., 1., 1.])
            #     ax.set_axis_off()
            #     fig.add_axes(ax)
            #     plt = Palette('palettes/' + gp.pp.palette) 
            #
            #     # Repeat for each package in the layer
            #     while (actual_position < end_position):
            #         packet_code = read_half_unsigned(gp.binaryfile)
            #         package = PACKAGES[packet_code](gp)                
            #         package.plot(ax, plt)
            #         actual_position = gp.binaryfile.tell()    
            #
            #     fig.savefig('images/' + self.gp.RADAR_ID + '/' + gp.file_name, transparent=gp.pp.transparent, dpi=my_dpi)

            
