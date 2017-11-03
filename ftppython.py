import ftplib
import os

def ftpTest():

    HOST='52.178.47.28'
    ID= 'HelperWEB\shin_root'
    PASSWORD='fnfnffn94'

    ftp = ftplib.FTP(HOST)
    ftp.login(ID, PASSWORD)

    #ftp file location
    mainlocation = "./Image"
    ftp.cwd(mainlocation)

    #local file location
    fname = "./Image/test.cgi"
    #os.chdir(r + fname)
    myfile = open(fname, 'r')

    create_file = '/target.cgi'
    fileToStore = mainlocation + create_file
    ftp.storlines('STOR ' + fileToStore, myfile)

    ftp.quit()
    myfile.close()

ftpTest()