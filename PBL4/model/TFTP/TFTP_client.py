import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

# from tftpy import TftpClient
# from model.global_resources import host
from model.global_resources import root_directory_path, tftp
import os

class TFTP_Client:
    def __init__(self):
        # self.tftp_client = TftpClient(host)
        self.tftp_client = tftp

    def upload_file_TFTP(self, local_file_path, name_remote_file):
        try:
            remote_file_path = os.path.join(root_directory_path, name_remote_file)
            self.tftp_client.upload(remote_file_path, local_file_path)
            return True
        except Exception as e:
            print(str(e))
            return False

    def download_file_TFTP(self, name_remote_file, local_directory_path):
        try:
            remote_file_path = os.path.join(root_directory_path, name_remote_file)
            local_file_path = os.path.join(local_directory_path, name_remote_file)
            self.tftp_client.download(remote_file_path, local_file_path)
            return True
        except Exception as e:
            print(str(e))
            return False

