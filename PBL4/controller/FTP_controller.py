import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

from model.FTP.FTP_Client import FTPClient

class FTPController:
    def login_ftp(self, username, password):
        # Gọi phương thức connect trong Model để thực hiện kết nối FTP
        connected, output = FTPClient().connect(username, password)
        if connected:
            list_files_in_directory = tuple(reversed(FTPClient().list_files_and_directory("/")))
            return True, list_files_in_directory, ""
        else:
            return False, None, output
    
    def logout_ftp(self):
        FTPClient().disconnect()
        
    def upload_FTP(self, remote_directory, local_file_path):
        upload, output = FTPClient().upload_file_FTP (remote_directory, local_file_path)
        if upload:
            list_files_in_directory = tuple(reversed(FTPClient().list_files_and_directory("/")))
            return True, list_files_in_directory, output
        else:
            return False, None, output
    
    def download_FTP(self, remote_directory, local_download_path):
        return FTPClient().download_file_FTP(remote_directory, local_download_path)

    def creat_folder(self, remote_directory):
        creat, output = FTPClient().create_directory(remote_directory)
        if creat:
            list_files_in_directory = tuple(reversed(FTPClient().list_files_and_directory("/")))
            return True, list_files_in_directory, output
        else:
            return False, None, output
    
    def rename(self, remote_old_path, remote_new_path):
        creat, output = FTPClient().rename(remote_old_path, remote_new_path)
        if creat:
            list_files_in_directory = tuple(reversed(FTPClient().list_files_and_directory("/")))
            return True, list_files_in_directory, output
        else:
            return False, None, output
    
    def delete(self, remote_path):
        delete, output = FTPClient().delete(remote_path)
        if delete:
            list_files_in_directory = tuple(reversed(FTPClient().list_files_and_directory("/")))
            return True, output, list_files_in_directory
        else:
            return False, output, None
