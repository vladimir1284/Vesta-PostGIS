'''
Created on 11/04/2013

@author: vladimir
'''
from Phenomenon.Phenomena import Phenomena
import logging

logger = logging.getLogger("Tornado")

class Tornado(Phenomena):
    def __init__(self,ipos,jpos,elevated,gp):
        Phenomena.__init__(self,ipos,jpos,gp)
        self.elevated = int(elevated)
    
    def set_id(self,cell):
        self.storm_id = cell
        self.commit()
               
    def commit(self):
        try:
            query_str = """SELECT insert_tvs_product(
                            '%s', '%s', '%s', %i, '%s', '%s',
                            ST_GeomFromText('POINT(%s)',2085));""" \
                            %(self.gp.datetime, self.gp.RADAR_ID,
                              self.storm_id, self.elevated, self.data, self.adata,
                              self.point)
            logger.debug(query_str)
            self.DB_CONN.query(query_str)
            
        except:
            logger.error(self.DB_CONN.error)  
#             print '\n In function commit from class Tornado\n'