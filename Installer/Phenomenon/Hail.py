'''
Created on 11/04/2013

@author: vladimir
'''

from Phenomenon.Phenomena import Phenomena
import logging

logger = logging.getLogger("Hail")

class Hail(Phenomena):
    '''
    classdocs
    '''

    def __init__(self,ipos,jpos,prob,prob_sevr,m_size,gp):
        '''
        Constructor
        '''
        Phenomena.__init__(self,ipos,jpos,gp)
                
        self.hail_probability = prob
        self.hail_severe_probability = prob_sevr
        self.hail_max_size = m_size
        self.ipos = ipos
        self.jpos = jpos
    
    def set_id(self,cell_id,ipos,jpos):
        if (ipos==self.ipos)&(jpos==self.jpos):
            self.storm_id = cell_id
            self.commit()
        else:
            logger.error("Error, Storm ID out of position\n" + 
                         "Hail ipos: %i \t jpos: %i" % (self.ipos,self.jpos) +
                         "Storm ID (package 8) ipos: %i \t jpos: %i" % (ipos,jpos))        
        
    def commit(self):
        if (self.hail_severe_probability >= 50): hail_symbol = 0
        elif (self.hail_severe_probability >= 30): hail_symbol = 1
        elif (self.hail_probability >= 50): hail_symbol = 2
        elif (self.hail_probability >= 30): hail_symbol = 3
        else: hail_symbol = 5
        
        if (self.hail_max_size == 0): 
            hail_symbol_text = "*"
        else:
            hail_symbol_text = "%i" % self.hail_max_size
        
        
        query_str = """SELECT insert_hi_product(
                    '%s', '%s', '%s', %i, %i, %i, %i, '%s', '%s', '%s',
                    ST_GeomFromText('POINT(%s)',2085));""" \
                    %(self.gp.datetime,self.gp.RADAR_ID,
                      self.storm_id, self.hail_probability,
                      self.hail_severe_probability, self.hail_max_size, 
                      hail_symbol, hail_symbol_text, self.data, self.adata,
                      self.point)
        logger.debug(query_str)
        
        try:
            self.DB_CONN.query (query_str)
        except:
            try:
                logger.error(self.DB_CONN.error)
            except:
                logger.error("There is no database connection")
            