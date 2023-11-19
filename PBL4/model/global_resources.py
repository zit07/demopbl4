# global_resources.py
import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

from model.FTP.FTP_handler import FTPHandler
import paramiko


#config
host = "192.168.64.10"
portFTP = 21
root_directory_path = "/srv/tftp"
directoryIMG = "/Users/haison/Downloads/ky7/TestFTP/PBL4/view/IMG/"
filenamelist= ["doc", "document", "docx", "file", "folder", "jpeg", "jpg", "pdf", "png", "sourcecode", "sql", "xls", "zip", "xlsx"]

ftp = FTPHandler(host, portFTP)

#Chieu rong va chieu cao cua so chinh
x = 1000
y = 700 

ssh = paramiko.SSHClient()
portSSH = 22
class UsernameSSH:
    usernameSSH = ""
    @classmethod
    def set_username(cls, username):
        cls.usernameSSH = username
    @classmethod
    def get_username(cls):
        return cls.usernameSSH
    
class UsernameSSH_Root:
    usernameSSH = "son"
    @classmethod
    def get_username_root(cls):
        return cls.usernameSSH
    