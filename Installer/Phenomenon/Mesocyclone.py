'''
Created on 12/04/2013

@author: vladimir
'''
from Phenomenon.Phenomena import Phenomena
import logging

logger = logging.getLogger("Mesocyclone")

class Mesocyclone(Phenomena):
    def __init__(self,ipos,jpos,FeatureType,attribute,gp):
        Phenomena.__init__(self,ipos,jpos,gp)
        
        self.strength_rank = attribute
        self.commited = False
        
        '''
        FeatureType
        9 = MDA Circulation with Strength Rank >= 5 AND with a Base Height <= 1 km ARL 
        or with its Base on the lowest elevation angle.
        10 = MDA Circulation with Strength Rank >= 5 AND with a Base Height > 1 km ARL
        AND that Base is not on the lowest elevation angle.
        11 = MDA Circulation with Strength Rank < 5
        '''
        self.FeatureType = FeatureType
    
    def set_id(self,meso_id,ipos,jpos):
        if (ipos==self.ipos)&(jpos==self.jpos):
            self.meso_id = int(meso_id)
        else:
            logger.error("Error, Mesocyclone ID out of position\n" +
                         "Mesocyclone ipos: %i \t jpos: %i" % (self.ipos,self.jpos) +
                         "ID (package 8) ipos: %i \t jpos: %i" % (ipos,jpos))
            
        
    def commit(self):
        self.checkLines()
        query_str = """SELECT insert_md_product('%s', '%s', %i, %i, %i, 
                '%s', '%s', ST_GeomFromText('LINESTRING(%s)',2085), 
                ST_GeomFromText('LINESTRING(%s)',2085), 
                ST_GeomFromText('POINT(%s)',2085));""" %\
              (self.gp.datetime,self.gp.RADAR_ID,
               self.strength_rank,self.FeatureType, self.meso_id,
               self.data, self.adata, self.line_past, self.line_forecast, 
               self.point)
        logger.debug(query_str) 
        try:
            self.DB_CONN.query(query_str)        
            self.commited = True
        except:
            logger.error(self.DB_CONN.error)
            
