import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

from model.TFTP.TFTP_handler import TFTPClient
from model.global_resources import host
from model.global_resources import root_directory_path
import os

class TFTPHandler:
    def __init__(self):
        self.tftp_client = TFTPClient(host)

    def upload_file_TFTP(self, local_file_path, name_remote_file):
        try:
            remote_file_path = os.path.join(root_directory_path, name_remote_file)
            self.tftp_client.upload_file(remote_file_path, local_file_path)
            return True
        except Exception as e:
            print(str(e))
            return False

    def download_file_TFTP(self, name_remote_file, local_directory_path):
        try:
            remote_file_path = os.path.join(root_directory_path, name_remote_file)
            local_file_path = os.path.join(local_directory_path, name_remote_file)
            self.tftp_client.download_file(remote_file_path, local_file_path)
            return True
        except Exception as e:
            print(str(e))
            return False

