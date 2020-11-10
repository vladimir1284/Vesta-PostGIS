'''
Created on 10/04/2013

@author: vladimir
'''
import ftplib
import traceback
import logging

logger = logging.getLogger("ImageUpload")

class ImageUpload:
    #TODO hacer login una sola vez
    def __init__(self,host,user,passwd):
        self.ftp = ftplib.FTP()
        self.ftp.connect(host)#'vesta-web')
        logger.debug(self.ftp.getwelcome())
        self.cd = True
        
        try:
            self.ftp.login(user,passwd)#'vesta_web_ftp', 'billar')
        except:
            logger.error('Connection error to FTP')
            
    def upload(self, f, file_name, dirname):
        try:    
            if self.cd:            
                dirs = dirname.split('/')
                for folder in dirs:
                    try:
                        self.ftp.cwd(folder)
                    except:
                        try:
                            self.ftp.mkd(folder)
                            self.ftp.cwd(folder)
                        except:
                            class Myfile:
                                def __init__(self):
                                    pass
                                def write(self,txt):
                                    logger.error(txt)
                            logger_file = Myfile()
                            traceback.print_exc(file = logger_file)
                logger.debug("Currently in:" + self.ftp.pwd())
    
            logger.debug("Uploading...")
            self.ftp.storbinary('STOR ' + file_name, f)
            self.cd = False # No need for changing directory again
            f.close()
            logger.debug("OK")
            self.ok = True
        except:
            logger.debug("Quitting...")
            self.ftp.quit()
            self.ok = False
            
    def disconnect(self):
        self.ftp.quit()