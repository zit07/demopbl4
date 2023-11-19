import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

from model.tftp_handler import TFTPHandler

class TFTPController:
    def upload_TFTP(self, local_file_path, name_remote_file):
        return TFTPHandler().upload_file_TFTP(local_file_path, name_remote_file)

    def download_TFTP(self, local_directory_path, name_remote_file):
        return TFTPHandler().download_file_TFTP(name_remote_file, local_directory_path)