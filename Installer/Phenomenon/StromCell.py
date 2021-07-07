'''
Created on 13/04/2013

@author: vladimir
'''
from Phenomenon.Phenomena import Phenomena
import logging
import psycopg2 as pg

logger = logging.getLogger("StormCell")

class StormCell(Phenomena):
    def __init__(self,ipos,jpos,storm_id,gp):
        Phenomena.__init__(self,ipos,jpos,gp)
        
        self.storm_id = storm_id
        self.commited = False
        
        
    def commit(self):
        # Get adata id if exist, insert otherwise
        query_sel = """SELECT ID from public.vestaweb_adaptationdata where 
                    body = '%s'""" % self.gp.adata
        query_ins = """INSERT INTO public.vestaweb_adaptationdata(body)
                        VALUES ('%s') RETURNING id""" % self.gp.adata
        logger.debug(query_sel)
        adata_id = 0
        try:      
            cur = self.gp.DB_CONN.cursor()
            cur.execute(query_sel)
            adata_id = cur.fetchone()           
            if (adata_id):
                adata_id = adata_id[0]
            else:
                cur.execute(query_ins)
                self.gp.DB_CONN.commit()
                adata_id = cur.fetchone()[0]
                logger.debug(query_ins)
        except (Exception, pg.DatabaseError) as error:
            logger.error(error)
            
        # Insert storm tracking information
        if (len(self.line_past)>0):
            past_Ipos = ('{'+''.join('%i, '%x[0] for x in self.line_past[1:]))[:-2] +'}'
            past_Jpos = ('{'+''.join('%i, '%x[1] for x in self.line_past[1:]))[:-2] +'}'
        else:
            past_Ipos = '{}'
            past_Jpos = '{}'
            
        if (len(self.line_forecast)>0):
            forecast_Ipos = ('{'+''.join('%i, '%x[0] for x in self.line_forecast[1:]))[:-2] +'}'
            forecast_Jpos = ('{'+''.join('%i, '%x[1] for x in self.line_forecast[1:]))[:-2] +'}'
        else:
            forecast_Ipos = '{}'
            forecast_Jpos = '{}'  
            
        radar_id = "(SELECT id from vestaweb_radar WHERE radar_code='%s')" % self.gp.RADAR_ID
        
        query_str = """INSERT INTO public.vestaweb_stormtracking(created, label, 
                    "Ipos", "Jpos", "past_Ipos", "past_Jpos", "forecast_Ipos", 
                    "forecast_Jpos", radar_id) VALUES ('%s', '%s', %i, %i, '%s', 
                    '%s', '%s', '%s', %s)""" % (self.gp.datetime, self.storm_id,
                    self.ipos, self.jpos, past_Ipos, past_Jpos, forecast_Ipos, 
                    forecast_Jpos, radar_id)
        logger.debug(query_str)
        
        try:      
            cur = self.gp.DB_CONN.cursor()
            cur.execute(query_str)
            self.gp.DB_CONN.commit()
            logger.debug(query_str)
        except (Exception, pg.DatabaseError) as error:
            logger.error(error)
              
            