'''
Created on 13/04/2013

@author: vladimir
'''
from Phenomenon.Phenomena import Phenomena
import logging

logger = logging.getLogger("StormCell")

class StormCell(Phenomena):
    def __init__(self,ipos,jpos,storm_id,gp):
        Phenomena.__init__(self,ipos,jpos,gp)
        
        self.storm_id = storm_id
        self.commited = False
        
        
    def commit(self):
        self.checkLines()
        
        query_str = """SELECT insert_sti_product('%s', '%s', '%s','%s',
                '%s', ST_GeomFromText('LINESTRING(%s)',2085),
                ST_GeomFromText('LINESTRING(%s)',2085),
                ST_GeomFromText('POINT(%s)',2085));""" %\
                (self.gp.datetime,self.gp.RADAR_ID,
                 self.storm_id,self.data, self.adata, self.line_past, 
                 self.line_forecast, self.point)
        logger.debug(query_str)
        try:
            self.DB_CONN.query(query_str)        
            self.commited = True
        except:
            logger.error(self.DB_CONN.error)
            #print '\n In function commit from class StromCell\n'   
            