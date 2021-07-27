'''
Created on 11/04/2013

@author: vladimir
'''
from ProductBlocks import read_half, read_word
from SiteConfiguration import OFFSET
import logging

MAX_NUM_LINES = 17

logger = logging.getLogger("TabularAlphanumericBlock")

class TabularAlphanumericBlock:
    def __init__(self,gp):
        
        binaryfile = gp.binaryfile
        binaryfile.seek(OFFSET + gp.pdb.tab_off*2, 0)
        
        
        divider = read_half(binaryfile)
        bid = read_half(binaryfile)
        blen = read_word(binaryfile)
        
        len_read = 0
        page_parse_error=False
        if (divider != -1) | (bid != 3):
            print("TAB  ERROR\nERROR Entering TAB Block, Either entry offset\n is incorrect or TAB divider and ID are Incorrect")
        else:
            # advance offset pointer beyond the message header block and the
            # product description block
            binaryfile.seek(120,1)
            
            blok_divider = read_half(binaryfile)
            numpages = read_half(binaryfile)
            
            for i in range(numpages):
                adapt = False
                
                while True:
                    num = read_half(binaryfile)  # num of chars in current line
                    if num == -1 : break # Romper si llega al final
                    line = binaryfile.read(num).decode("utf-8") 
                    if (line.find("ADAPTATION") != -1) or \
                        (line.find("ADAPTABLE") != -1) or \
                        (line.find("ALTITUDES SELECTED") != -1) or adapt:
                        adapt = True # The entire page is adaptation data
                        gp.adata += line + '\n'
                    else:
                        gp.data += line + '\n'
#             f = open("adata.txt",'w')
#             f.write(gp.adata)
#             f.close()
#             f = open("data.txt",'w')
#             f.write(gp.data)
#             f.close()   
#                 else:                        
#                     process=True
#                     num_lines = 0
#                     while(process):
#                         num = read_half(binaryfile)
#                         len_read = len_read +2 + num
#                         
#                         if(len_read >= blen):
#                             print "TAB  ERROR\nERROR PARSING TAB PAGE Number %i\nNumber of Characters to be read exeeds block length\n" % i
#                             page_parse_error = True
#                             break
#     
#           
#                         if(num > 80):
#                             print "TAB  ERROR\nERROR PARSING TAB PAGE Number %i\nNumber of Characters Exceed 80 on Line %i\n" % (i, num_lines+1)
#                             page_parse_error = True
#                             break
#     
#               
#                          if a max size page we exit after checking for divider   
#                         if(num_lines==MAX_NUM_LINES):
#                             if(num==-1):
#                                 break 
#                             else:
#                                 print "TAB  ERROR\nERROR PARSING TAB PAGE Number %i\n or Number of Lines Exceed Limit of 17\nDid Not Find End-Of-Page (-1) Divider\n" % i
#                                 page_parse_error = True
#                                 break
#      
#            
#                         if(num==-1): break  # catch a short page
#                
#                         line = binaryfile.read(num)
#                         print line
#                         num_lines += 1
#                     if(page_parse_error==True):
#                         break
            
