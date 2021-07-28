# -*- coding: utf-8 -*-
'''
Created on 08/04/2013

@author: vladimir
'''
from ProductBlocks.ProductDescriptionBlock import ProductDescriptionBlock
from ProductProperties import ProductProperties
from ProductBlocks.SymbologyBlock import *
from ProductBlocks.TabularAlphanumericBlock import TabularAlphanumericBlock
from ImageUpload import ImageUpload
from SiteConfiguration import OFFSET
from ProductBlocks.StandAloneTabularAlphanumeric import StTabularAlphanumeric
from Phenomenon.CellTrend import Cell_trend_data

import psycopg2 as pg
from time import gmtime
import time

SECS_PER_DAY = 86400 # Number of seconds in a day

PCODES = {94: 'DR_94', 99: 'DV_99', 155: 'SDW_155', 137: 'ULR_137', 62: 'SS_62', 58: 'STI_58'}

logger = logging.getLogger("GraphicProduct")

class GraphicProduct:
    '''
    classdocs
    '''

    def __init__(self, binaryfilename, ppfilename,RADAR_ID):
        '''
        Constructor
        '''
        start_time = time.time()
        self.RADAR_ID = RADAR_ID
        
        self.binaryfile = open(binaryfilename,'rb')
        self.images = []
        self.georeference = []
        self.adata = ''
        self.data = ''
        
        # Database connection
        self.DB_CONN = pg.connect(database='vesta-web', host='localhost', 
                                  user='vesta', password='billar')
        
        # Parsing Product Description Block
        self.pdb = ProductDescriptionBlock(self)
        pcode = self.pdb.MH_msg_code
        self.pcode = PCODES[pcode]
        
        # Getting  Product Properties
        self.pp = ProductProperties(ppfilename, pcode)
        
        logger.debug(self.pp.getProperties())
            
        # Hora de la observacion
        self.vol_time = gmtime((self.pdb.vol_date-1)*SECS_PER_DAY + 
                               self.pdb.vol_time_ms*0xffff + 
                               self.pdb.vol_time_ls) 
        
        self.dirname =  RADAR_ID+"/%s_%i/%04i/%02i/%02i" % (self.pp.name,
                        pcode, self.vol_time.tm_year, self.vol_time.tm_mon, 
                        self.vol_time.tm_mday)
        self.file_name = "%s_%s_%04i-%02i-%02i_%02i-%02i-00" % (self.pp.name, 
                        pcode,self.vol_time.tm_year, self.vol_time.tm_mon,
                        self.vol_time.tm_mday,self.vol_time.tm_hour,
                        self.vol_time.tm_min)
        self.datetime = "%04i-%02i-%02i %02i:%02i:00" % (self.vol_time.tm_year, 
                        self.vol_time.tm_mon,self.vol_time.tm_mday,
                        self.vol_time.tm_hour, self.vol_time.tm_min)

        # self.radar_pj = pj.Proj(proj="aeqd", lat_0=RADAR_LOCATIONS[RADAR_ID][0], 
        #                         lon_0=RADAR_LOCATIONS[RADAR_ID][1], 
        #                         datum="WGS84", units="m")
        
        logger.debug('\nDir name:\t' + self.dirname +'\n'+
                     'File name:\t' + self.file_name +'\n'+
                     'Datetime:\t' + self.datetime +'\n')
                    
        # Tabular Alphanumeric Block
        if self.pdb.tab_off != 0:
            self.tb = TabularAlphanumericBlock(self)
            
        # Parse Symbology Block or StTabularAlphanumeric
        if self.pdb.sym_off != 0:
            if self.pp.stand_alone:
                self.st = StTabularAlphanumeric(self)
            else:
                start_sb = time.time()
                self.sb = SymbologyBlock(self)
                logger.debug('Parse Symbology Block: %ims' % int(1e3*(time.time()
                                                                      -start_sb)))
                
        # Cell Trend data for SS
        if pcode == 62:
            # Check for any storm present
            binaryfile = self.binaryfile
            binaryfile.seek(OFFSET + self.pdb.gra_off*2,0)
            if len(binaryfile.read(2)) != 0:
                ct = Cell_trend_data(self)
                ct.upload(self.st)
        
       

    def upload(self):
        if self.pp.geographic:
            query_str = """INSERT INTO public.vestaweb_rasterproduct(
                        created, description_id, radar_id) VALUES 
                        ('%s', (SELECT id from vestaweb_productdescription 
                        WHERE pcode='%s'), (SELECT id from vestaweb_radar WHERE 
                        radar_code='%s')) """ % (self.datetime, self.pcode,
                                              self.RADAR_ID)
            logger.debug(query_str)
            try:      
                cur = self.DB_CONN.cursor()
                cur.execute(query_str)
                self.DB_CONN.commit()
            except (Exception, pg.DatabaseError) as error:
                logger.error(error)

        # Upload Images
#         start_ftp = time.time()
#
#         if self.images: iu = ImageUpload('vesta-web',
#                                          'vesta_web_ftp', 
#                                          'billar') # Connect if necessary
#         for image in self.images:
#             fig_file = open('images/'+self.RADAR_ID+'/'+image, 'rb')
#             iu.upload(fig_file, image, self.dirname)
#             if iu.ok:
#                 subprocess.getoutput('rm images/'+self.RADAR_ID+'/'+image)
#         fig_file.close()
#
#         if self.pp.geographic:
#             wfile = open('images/'+self.RADAR_ID+'/'+image+'w', 'rb')
#             iu.upload(wfile, image+'w', self.dirname)
#             if iu.ok:
#                 subprocess.getoutput('rm images/'+self.RADAR_ID+'/'+image+'w')
#             wfile.close()
#
#
#         if self.images: iu.disconnect()  # Disonnect if connected  
#
#         logger.debug('FTP image upload time: %ims' % int(1e3*(time.time()
#                                                                -start_ftp)))
#
#
#         # Feed Vesta|Mosaic
#         if self.pp.mosaic_name != '':
#             self.binaryfile.close()
#
#             start_ftp = time.time()
#             pfile = open(binaryfilename,'rb')
#             if self.images: iu = ImageUpload('vesta-mosaic',
#                                              'vesta_mosaico_ftp', 
#                                              'ganador') # Connect if necessary
#
#             pdirname = RADAR_ID + '/' + self.pp.mosaic_name
#             pname = self.pp.mosaic_name + '_' + \
#                      "%04i%02i%02i_%02i%02i" % (self.vol_time.tm_year, 
#                          self.vol_time.tm_mon,self.vol_time.tm_mday,
#                          self.vol_time.tm_hour, self.vol_time.tm_min)
# #            now_time = gmtime(time.time())
# #            pname = self.pp.mosaic_name + '_' + \
# #                    "%04i%02i%02i_%02i%02i" % (now_time.tm_year, 
# #                        now_time.tm_mon,now_time.tm_mday,
# #                        now_time.tm_hour, now_time.tm_min)      
#             iu.upload(pfile, pname, pdirname)
#             if self.images: iu.disconnect()  # Disonnect if connected  
#
#             logger.debug('FTP product upload time: %ims' % int(1e3*(time.time()
#                                                                    -start_ftp)))
#
#         logger.debug('Total product time: %ims' % int(1e3*(time.time()-start_time))
#                      + '\n\n')