'''
Created on 13/04/2013

@author: vladimir
'''
from Binary_Packages import read_half
import struct
from SiteConfiguration import OFFSET

class StTabularAlphanumeric:
    def __init__(self,gp):
        self.gp = gp
        self.gp.binaryfile.seek(OFFSET + gp.pdb.sym_off*2, 0)
        s = gp.binaryfile.read(4) # Leer como string
        (block_divider, self.number_of_pages)=struct.unpack('>2h',s)
        self.scan_data()
#         if DATABASE:
#             self.insert_db()
        
    def scan_data(self):
        self.gp.data = ''
        self.gp.adata = ''
        is_adata = False
        u = 0
        count = 0
        self.cell_location = {} # cell_id -> [azimut, range]
        for i in xrange(self.number_of_pages):
            while True:
                num = read_half(self.gp.binaryfile)  # num of chars in current line
                if num == -1 : # Romper si llega al final
                    break 
                line = self.gp.binaryfile.read(num)                    
                if (line.find("ADAPTATION") != -1 or 
                    is_adata):  
                    is_adata = True                  
                    self.gp.adata += line +"\n"
                else:
                    if (line.find("STORM STRUCTURE") != -1):
                        u = 0
                    if u < 6:
                        u += 1
                    else:
                        if (line.find("/") == -1):
                            u = 10
                        if u != 10:
                            a = line.split('    ')
                            b = a[2].split('/')
                            try:
                                self.cell_location.setdefault(a[1].split()[0],
                                                              [int(b[0]), int(b[1])])
                            except:
                                self.cell_location.setdefault(a[1].split()[0],[0, 0])
                    self.gp.data += line +"\n"

        f = file("adata.txt",'w')
        f.write(self.gp.adata)
        f.close()
        f = file("data.txt",'w')
        f.write(self.gp.data)
        f.close()            
                
#     def insert_db(self):
#         try:
#             self.res = self.DB_CONN.query("INSERT INTO ss_adaptation_data(data) VALUES('%s');" % self.adata)
#             self.res = self.DB_CONN.query("SELECT id from ss_adaptation_data WHERE data='%s';" % self.adata);
#             self.adata_id = self.res.getresult()[0][0]
#             self.res = self.DB_CONN.query("INSERT INTO ss_data(datetime, data, adaptation_data_id) VALUES('%s','%s',%i);" % (self.gp.datetime, self.data, self.adata_id))
# 
#         except:
#             print self.DB_CONN.error
