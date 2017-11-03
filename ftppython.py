import ftplib
import os

def ftpTest():

    HOST='52.178.47.28'
    ID= 'HelperWEB\shin_root'
    PASSWORD='fnfnffn94'

    ftp = ftplib.FTP(HOST)
    ftp.login(ID, PASSWORD)

    #ftp file location
    mainlocation = "/site/wwwroot"
    ftp.cwd(mainlocation)

    #local file location
    fname = "./Image/test.cgi"
    #os.chdir(r + fname)
    myfile = open(fname, 'rb')

    #targetfile to create on ftp
    create_file = 'target.cgi'
    ftp.storlines('STOR ' + create_file, myfile)

    ftp.quit()
    myfile.close()

ftpTest()