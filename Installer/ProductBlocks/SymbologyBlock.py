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
from osgeo import gdal
from osgeo import osr
import os
os.environ['GDAL_DATA'] = " /usr/share/gdal"

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
            gp.binaryfile = StringIO(symb_string)  # Handle string as file         

        blockHeader = struct.unpack('>hHiH', gp.binaryfile.read(10))
        self.divider = blockHeader[0]  # value of -1 used to delineate the following from 
                                            # the above product description block; DIV2OFF 61
        self.block_id = blockHeader[1]  # always 1 
        self.block_len = blockHeader[2]  # length of this block in bytes including the 
                                            # preceding devider and block id; 1 - 80000 
        self.n_layers = blockHeader[3]  # number of data layers obtained in this block; 
                                            # 1 - 15     
        
        # for i in xrange(self.n_layers):
        layerHeader = struct.unpack('>hi', gp.binaryfile.read(6))  
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
                my_dpi = 1.0
                self.nPixels = int(1e3 * gp.pp.range / gp.pp.resolution)
                figureSize = (self.nPixels / my_dpi, self.nPixels / my_dpi)
                
                # GeoTiff generation
                # create the 1-band raster file
                self.dst_ds = gdal.GetDriverByName('GTiff').Create('images/' + self.gp.RADAR_ID + '/' + gp.file_name.split('.')[0]+'.tif', self.nPixels, self.nPixels, 1, gdal.GDT_Byte) 
                # Georeference
                geotransform = (-gp.pp.resolution*self.nPixels/2.0, gp.pp.resolution, 0, gp.pp.resolution*self.nPixels/2.0, 0, -gp.pp.resolution)
                self.dst_ds.SetGeoTransform(geotransform)    # specify coords
                srs = osr.SpatialReference()            # establish encoding
                srs.ImportFromProj4("+proj=aeqd +lat_0=%f +lon_0=%f +x_0=0 +y_0=0 +units=m +datum=NAD27" % (gp.pdb.latitude, gp.pdb.longitude))
                self.dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file   
            else:
                figureSize = (8, 8)  # Bigger for VAD & VWP
                my_dpi = 150.0
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
                    
            # fig = pylab.figure(figsize=figureSize, dpi=my_dpi)
            fig = pylab.figure(figsize=figureSize, dpi=my_dpi)
            ax = pylab.Axes(fig, [0., 0., 1., 1.])
            ax.set_axis_off()
            fig.add_axes(ax)
            # ax = pylab.axes(axisbg = 'w', polar=gp.pp.polar)
            plt = Palette('palettes/' + gp.pp.palette)
            
            # Load data and colors
            self.band = self.dst_ds.GetRasterBand(1)
            self.band.SetNoDataValue(0)             
            colors = VestaColorTable('palettes/' + gp.pp.palette)
            self.band.SetRasterColorTable(colors)
            self.band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
            
            # Repeat for each package in the layer
            while (actual_position < end_position):
                packet_code = read_half_unsigned(gp.binaryfile)
                package = PACKAGES[packet_code](gp)                
                package.plot(ax, plt)
                package.writeData(self.band)   # write r-band to the raster
                actual_position = gp.binaryfile.tell()    
                            
            # pylab.xticks([])
            # pylab.yticks([])
            # pylab.axis(gp.pp.axis)
            # if gp.pp.polar: 
            #     pylab.axis('off')
            fig.savefig('images/' + self.gp.RADAR_ID + '/' + gp.file_name, transparent=gp.pp.transparent, dpi=my_dpi)
            # fig.savefig('images/' + self.gp.RADAR_ID + '/' + gp.file_name, format='png', bbox_inches='tight',
            #             pad_inches=0, transparent=gp.pp.transparent, dpi=my_dpi)  # 396.5)
            
            
            # write to disk
            self.dst_ds.FlushCache()                     
            self.band = None
            self.dst_ds = None  

        if gp.pp.geographic:
            wfile = file('images/' + self.gp.RADAR_ID + '/' + gp.file_name + 'w', 'w')
            wfile.write(self.georeference())
            wfile.close()

            gp.images.append(gp.file_name)

    def georeference(self): 
        # nPixels = self.gp.pp.range / self.gp.pp.resolution
        # [minx, miny, maxx, maxy] = self.gp.georeference[0]
        [proj_p_ur, proj_p_ll, proj_p_ul, proj_p_lr] = self.gp.georeference[0]
        print ("UR: %i,%i" % (proj_p_ur[0]/1000, proj_p_ur[1]/1000))
        print ("LL: %i,%i" % (proj_p_ll[0]/1000, proj_p_ll[1]/1000))
        print ("UL: %i,%i" % (proj_p_ul[0]/1000, proj_p_ul[1]/1000))
        print ("LR: %i,%i" % (proj_p_lr[0]/1000, proj_p_lr[1]/1000))
        maxx = max(proj_p_ur[0], proj_p_lr[0])
        maxy = max(proj_p_ur[1], proj_p_ul[1])
        minx = min(proj_p_ul[0], proj_p_ll[0])
        miny = max(proj_p_lr[1], proj_p_ll[1])
        del_x = (maxx - minx) / (self.nPixels - 1)
        del_y = (maxy - miny) / (self.nPixels - 1)
        x_left = minx  # proj_p_ul[0]
        y_up = maxy  # proj_p_ul[1]
        return "%.2f\n0.0000000000\n0.0000000000\n-%.2f\n%.2f\n%.2f" % \
                (del_x, del_y, x_left, y_up) 
