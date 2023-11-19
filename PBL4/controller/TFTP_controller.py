import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

from model.TFTP.TFTP_client import TFTP_Client

class TFTPController:
    def upload_TFTP(self, local_file_path, name_remote_file):
        return TFTP_Client().upload_file_TFTP(local_file_path, name_remote_file)

    def download_TFTP(self, local_directory_path, name_remote_file):
        return TFTP_Client().download_file_TFTP(name_remote_file, local_directory_path)