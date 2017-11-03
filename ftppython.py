import ftplib
import os

def ftpSave(local_location, ftp_location, save_name):

    HOST='52.178.47.28'
    ID= 'HelperWEB\shin_root'
    PASSWORD='fnfnffn94'

    ftp = ftplib.FTP(HOST)
    ftp.login(ID, PASSWORD)

    #ftp file location
    mainlocation = "/site/wwwroot"
    ftp.cwd(mainlocation)

    #local file location
    #fname = "./Image/test.cgi"
    fname = local_location
    #os.chdir(r + fname)
    myfile = open(fname, 'rb')

    #targetfile to create on ftp
    #create_file = 'target.cgi'
    create_file = ftp_location + save_name
    ftp.storlines('STOR ' + create_file, myfile)

    ftp.quit()
    myfile.close()

#Local location, FTP location, Save file name
ftpSave("./Image/test.cgi", "Image/", "test.cgi")