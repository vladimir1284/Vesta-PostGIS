'''
Created on 13/04/2013

@author: vladimir
'''
import traceback
from Binary_Packages import read_half, read_byte
from SiteConfiguration import OFFSET
import pylab
from Binary_Packages.package_21 import Package_21
import struct
import logging
import psycopg2 as pg

logger = logging.getLogger("Cell_trend_data")

class Cell_trend_data:
    def __init__(self, gp):
        self.gp = gp
        binaryfile = gp.binaryfile
        binaryfile.seek(OFFSET + gp.pdb.gra_off*2,0)
        self.time = []
        self.cells = []
        
        # Leyendo las horas
        block_len =  read_half(binaryfile)
        num_vols =  read_byte(binaryfile)
        self.lts_vol_ptr_time = read_byte(binaryfile)
        for i in range(num_vols):
            minutes = read_half(binaryfile)
            self.time.append(minutes)
        
        # Leyendo los datos de las celdas
        while True:
            try:            
                s = binaryfile.read(2)
                if len(s) == 0: break # Fin del fichero
                packet_code = struct.unpack('>h',s)[0]
                block_len = read_half(binaryfile)   # Number of bytes to follow in
                                                    # this packet
                if packet_code == 21: 
                    trend_data = Package_21(binaryfile)
                else:
                    logger.error("""Error in packet_code (21 expected, %i found). 
                                    Prod 62""" % packet_code)
                    break
                self.cells.append(trend_data.cell)
            except:
                class Myfile:
                    def __init__(self):
                        pass
                    def write(self,txt):
                        logger.error(txt)
                logger_file = Myfile()
                traceback.print_exc(file = logger_file)
                break
    
    def  kft2km(self, x):
        return .305*x      
            
    def upload(self, st):
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
        
        # Insert storm cells
        for cell_trend in self.cells:
            [azimut, cell_range] = st.cell_location[cell_trend.cell_id]            
            tops = '{'+str(cell_trend.cell_top.tolist())[1:-1]+'}'
            bases = '{'+str(cell_trend.cell_base.tolist())[1:-1]+'}'
            max_ref_hgts = '{'+str(cell_trend.max_ref_hgt.tolist())[1:-1]+'}'
            centroids = '{'+str(cell_trend.centroid_hgt.tolist())[1:-1]+'}'
            poh = '{'+str(cell_trend.prob_hail.tolist())[1:-1]+'}'
            posh = '{'+str(cell_trend.prob_svr_hail.tolist())[1:-1]+'}'
            vil = '{'+str(cell_trend.cell_based_VIL.tolist())[1:-1]+'}'
            maxZ = '{'+str(cell_trend.max_ref.tolist())[1:-1]+'}'
            time = '{'+str(self.time)[1:-1]+'}'
            radar_id = "(SELECT id from vestaweb_radar WHERE radar_code='%s')" % self.gp.RADAR_ID
            
            query_str = """INSERT INTO public.vestaweb_stormcell(created, label,
                        azimut, range, tops, bases, max_ref_hgts, centroids, 
                        poh, posh, vil, "maxZ", time, adata_id, radar_id, 
                        lst_vol_time_ptr, lst_vol_data_ptr)
                        VALUES ('%s', '%s', %i, %i, '%s', '%s', '%s', '%s', '%s', '%s', '%s', 
                        '%s', '%s', %i, %s, %i, %i)""" % (
                            self.gp.datetime, cell_trend.cell_id, azimut, cell_range,
                            tops, bases, max_ref_hgts, centroids, poh, posh, vil, 
                            maxZ, time, adata_id, radar_id, self.lts_vol_ptr_time,
                            cell_trend.latest_vol)
            
            try:      
                cur = self.gp.DB_CONN.cursor()
                cur.execute(query_str)
                self.gp.DB_CONN.commit()
                logger.debug(query_str)
            except (Exception, pg.DatabaseError) as error:
                logger.error(error)

            
    def generate_images(self, st):
        SS_COVERAGE = self.gp.pp.range*0.53913 # From km to nm
        for cell_trend in self.cells:
            try:
                fig = pylab.figure(figsize=(6, 6))  
                          
                # ===== Ploteando posicion =====
                ax = pylab.subplot(2,2,1,axisbg = 'w') 
                [azimut, range] = st.cell_location[cell_trend.cell_id]
                coverage = pylab.Circle((0,0),radius=SS_COVERAGE, lw = 2, edgecolor = 'b', 
                                  facecolor = 'none')
                radar = pylab.Circle((0,0),radius=5, lw = 1, edgecolor = 'k', 
                               facecolor = 'none')
                
                ax.add_patch(coverage)
                ax.add_patch(radar)
                pylab.xlim([-SS_COVERAGE-3,SS_COVERAGE+3])
                pylab.ylim([-SS_COVERAGE-3,SS_COVERAGE+3])
                pos_x = range*pylab.sin(azimut*pylab.pi/180)
                pos_y = range*pylab.cos(azimut*pylab.pi/180)
                storm = pylab.Circle((pos_x,pos_y),radius=16, lw = 1, edgecolor = 'k', 
                                     facecolor = 'none')
                ax.add_patch(storm)
                pylab.plot(pos_x,pos_y,'kx', ms = 8)
                text_x = pos_x + 16
                if text_x > SS_COVERAGE - 20:
                    text_x = pos_x
                    text_y = pos_y + 16
                else:
                    text_y = pos_y
                pylab.text(text_x,text_y,cell_trend.cell_id,color ='k')
                
                pylab.xticks([])
                pylab.yticks([])
                
                titulo = '%s %02i/ %02i/ %4i %s:%s' % (self.gp.RADAR_ID, 
                        self.gp.vol_time.tm_mday, self.gp.vol_time.tm_mon, 
                        self.gp.vol_time.tm_year, self.times[-1][0:2], 
                        self.times[-1][2:4])
                titulo += '\nCELL ID: %s' % cell_trend.cell_id
                titulo += '\nAZRAN   %iDEG %iNM' % (azimut, range)
                pylab.title(titulo, color='k',horizontalalignment='left',x=0, fontsize=10)
                
                
                
                # ===== Ploteando alturas =====
                ax = pylab.subplot(2,2,2,axisbg = 'w')            
                pylab.ylabel('KFT')
                pylab.xlabel('TIME')
                
                pylab.plot(cell_trend.max_ref_hgt, 'ro-', label='DBZM HT', linewidth=2)
                pylab.plot(cell_trend.centroid_hgt, 'mD-', label='CENT HT', linewidth=2)
    
                N = len(cell_trend.cell_top) # Cantidad de Volumenes
                for i in range(N):
                    y = (cell_trend.cell_top[i] + cell_trend.cell_base[i])/2.
                    yerr = (cell_trend.cell_top[i] - cell_trend.cell_base[i])
                    #print (y,yerr)
                    #print cell_trend.cell_base[i]
                    pylab.errorbar(i,y,yerr,color = 'k',elinewidth = 1,capsize = 6,
                                   lolims=True)
              
                self.white_axes(ax,N)
                
                # leyenda
                leg = pylab.legend(loc = 'upper center', ncol = 2, frameon = False, 
                             bbox_to_anchor = (0.5, 1.2), numpoints = 1, 
                             title = 'TOP-BASE', columnspacing = 0.5, 
                             handletextpad = 0.3, prop = dict(size = 8))
                text1, text2 = leg.get_texts()
                # this part can be turned into a loop depends on the number of 
                # text objects
                text1.set_color('r')
                text2.set_color('m')
                leg.get_title().set_color('k')
                leg.get_title().set_fontsize(8)
                
                
                # ===== Ploteando Prob de Granizo =====
                ax = pylab.subplot(2,2,3,axisbg = 'w')            
                pylab.ylabel('PERCENT')
                pylab.xlabel('TIME')
                
                pylab.plot(cell_trend.prob_svr_hail, 'go-', label='POSH', linewidth=2)
                pylab.plot(cell_trend.prob_hail, 'kD-', label='POH', linewidth=2)
                                    
                self.white_axes(ax,N)
                
                # leyenda
                leg = pylab.legend(loc = 'upper center', ncol = 2, frameon = False,
                             bbox_to_anchor = (0.5, 1.1), numpoints = 1,
                             columnspacing = 0.5, handletextpad = 0.3, 
                             prop = dict(size = 8))
                text1, text2 = leg.get_texts()
                # this part can be turned into a loop depends on the number of 
                # text objects
                text1.set_color('g')
                text2.set_color('k')
                
                pylab.ylim([0,100])
                
                
                # ===== Ploteando VIL y MaxdBZ =====
                ax = pylab.subplot(2,2,4,axisbg = 'w')            
                pylab.ylabel('DBZ - KG/M**2')
                pylab.xlabel('TIME')
                
                pylab.plot(cell_trend.max_ref, 'ro-', label='DBZM', linewidth=2)
                pylab.plot(cell_trend.cell_based_VIL, 'bD-', label='CB VIL', linewidth=2)
                                    
                self.white_axes(ax,N)
                
                # leyenda
                leg = pylab.legend(loc = 'upper center', ncol = 2, frameon = False, 
                             bbox_to_anchor = (0.5, 1.1), numpoints = 1, 
                             columnspacing = 0.5, handletextpad = 0.3, 
                             prop = dict(size = 8))
                
                text1, text2 = leg.get_texts()
                # this part can be turned into a loop depends on the number of 
                # text objects
                text1.set_color('r')
                text2.set_color('b')
                
                # Saving figure  
                name = self.gp.file_name + '_%s' % cell_trend.cell_id + '.png'
                fig.savefig('images/'+self.gp.RADAR_ID+'/'+name, format='png', facecolor='w')
                self.gp.images.append(name)


                # Database update
                query_str = """SELECT insert_ss_product(
                                '%s','%s','%s','%s','%s','%s');""" % \
                                (self.gp.datetime, self.gp.RADAR_ID, 
                                 self.gp.dirname + '/' + name, 
                                 self.gp.data, self.gp.adata, cell_trend.cell_id)
                logger.debug(query_str)
                
                try:
                    self.gp.DB_CONN.query (query_str)
                except:
                    try:
                        logger.error(self.DB_CONN.error)
                    except:
                        logger.error("There is no database connection")
                    
            except:
                logger.info('Most probable no location for %s' % 
                            cell_trend.cell_id)
            
            
    def white_axes(self,ax,n):
        ax.tick_params(labelsize=4)
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(8)
        # horz grid
        ax.yaxis.grid(True, color = 'k')
        pylab.xticks(range(n),self.times)
        pylab.xlim([-0.1,n-0.9])
        
        
