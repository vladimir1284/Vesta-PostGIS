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

logger = logging.getLogger("Cell_trend_data")

class Cell_trend_data:
    def __init__(self, gp):
        self.gp = gp
        binaryfile = gp.binaryfile
        binaryfile.seek(OFFSET + gp.pdb.gra_off*2,0)
        self.times = []
        self.cells = []
        
        # Leyendo las horas
        block_len =  read_half(binaryfile)
        num_vols =  read_byte(binaryfile)
        lts_vol_ptr = read_byte(binaryfile)
        for i in xrange(num_vols):
            min = read_half(binaryfile)
            self.times.append('%02i%02i' % (min/60, pylab.mod(min,60)))
            #print self.times[i]
        
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
            
    def printData(self, st):
        SS_COVERAGE = self.gp.pp.range*0.53913 # From km to nm
        for cell_trend in self.cells:
            [azimut, range] = st.cell_location[cell_trend.cell_id]
                
            cell_str = "let %s = {'id': '%s', 'azimut':%i, 'range':%i,\n" %(cell_trend.cell_id, cell_trend.cell_id, azimut, range)
            cell_str += "'tops':["
            cell_str += "".join("%.1f, "%x for x in cell_trend.cell_top)
            cell_str +="],\n"
            cell_str += "'bases':["
            cell_str += "".join("%.1f, "%x for x in cell_trend.cell_base)
            cell_str +="],\n"
            cell_str += "'max_ref_hgts':["
            cell_str += "".join("%.1f, "%x for x in cell_trend.max_ref_hgt)
            cell_str +="],\n"
            cell_str += "'centroids':["
            cell_str += "".join("%.1f, "%x for x in cell_trend.centroid_hgt)
            cell_str +="],\n"
            cell_str += "'poh':["
            cell_str += "".join("%i, "%x for x in cell_trend.prob_hail)
            cell_str +="],\n"
            cell_str += "'posh':["
            cell_str += "".join("%i, "%x for x in cell_trend.prob_svr_hail)
            cell_str +="],\n"
            cell_str += "'vil':["
            cell_str += "".join("%i, "%x for x in cell_trend.cell_based_VIL)
            cell_str +="],\n"
            cell_str += "'maxZ':["
            cell_str += "".join("%i, "%x for x in cell_trend.max_ref)
            cell_str +="],\n"
            cell_str += "}"                
            print(cell_str)

            
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
                for i in xrange(N):
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
        
        
