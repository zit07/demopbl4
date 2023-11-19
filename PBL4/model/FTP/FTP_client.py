import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

from model.global_resources import ftp

class FTPClient:
    def connect(self, username, password):
        connect, output = ftp.connect()
        if connect == False:
            return False, output
        return ftp.login(username, password)
    
    def disconnect(self):
        try:
            ftp.quit()
            print("Disconnect FTP")
            return True
        except Exception as e:
            print(str(e))
            return False
        
    def upload_file_FTP(self, remote_directory, local_file_path):
        if ftp is None:
            return False, "Không có kết nối!"
        file_parts = local_file_path.split('/')
        remote_file_path = remote_directory + "/" + file_parts[-1]
        with open(local_file_path, "rb") as local_file:
            return ftp.storbinary(remote_file_path, local_file)

    def download_file_FTP(self, remote_file_path, local_file_path):
        if ftp is None:
            return False, "Không có kết nối!"
        with open(local_file_path, "wb") as local_file:
            return ftp.retrbinary(remote_file_path, local_file.write)
    
    def list_files_and_directory(self, remote_directory, parent_node=None, files_list_main=None):
        if files_list_main is None:
            files_list_main = []
        files_list = []
        try:
            lines = ftp.get_list_files_in_directory(remote_directory)
            for line in lines:
                parts = line.split(None, 8)
                if len(parts) < 9:
                    continue
                item_type, _, _, _, file_size, _, _, _, name = parts
                name = name.rstrip('\r')
                if item_type.startswith('d'):
                    files_list.append({"type": "folder", "directory": remote_directory, "name": name})
                    self.list_files_and_directory(remote_directory + '/' + name, parent_node, files_list_main)
                else:
                    files_list.append({"type": "file", "directory": remote_directory, "name": name, "size": int(file_size)})
        except Exception as e:
            print("Lỗi:", str(e))
            
        for items in files_list:
            files_list_main.append(items)
        
        return files_list_main

    def create_directory(self, remote_directory):
        if ftp.change_directory(remote_directory):
            return False, "Thư mục đã tồn tại"
        return ftp.mkd(remote_directory)
    
    def rename(self, remote_old_path, remote_new_path):
        if ftp.change_directory(remote_new_path):
            return False, "Tên này đã tồn tại trong thư mục"
        return ftp.rename(remote_old_path, remote_new_path)
        
    def delete(self, remote_path):
        try:
            if remote_path.startswith("/"):  # Đảm bảo rằng đường dẫn bắt đầu bằng "/"
                # Kiểm tra xem đường dẫn là thư mục hay tệp
                is_directory = ftp.change_directory(remote_path)
                if is_directory:
                    # Nếu là thư mục, xóa nó cùng với nội dung bên trong
                    self.delete_directory(remote_path)
                else:
                    # Nếu là tệp, xóa nó
                    delete, err = ftp.delete(remote_path)
                    if delete == False:
                        return False, f"Xoá thất bại, lỗi: {err}"
                return True, ""
            else:
                return False, "Đường dẫn không hợp lệ."
        except Exception as e:
            print(f"Lỗi khi xóa '{remote_path}': {str(e)}")
            return False, f"Xoá thất bại, lỗi: {str(e)}"

    def delete_directory(self, remote_path):
        # Xóa thư mục cùng với tất cả tệp và thư mục con bên trong
        try:
            # Liệt kê tất cả các tệp và thư mục bên trong thư mục
            items = self.list_files_and_directory(remote_path)
            for item in items:
                if item["type"] == "folder":
                    # Nếu là thư mục, gọi đệ quy để xóa thư mục con
                    self.delete_directory(item["directory"] + "/" + item["name"])
                else:
                    # Nếu là tệp, xóa tệp
                    ftp.delete(item["directory"] + "/" + item["name"])
            # Cuối cùng, xóa thư mục chính
            ftp.rmd(remote_path)
        except Exception as e:
            print(f"Lỗi khi xóa thư mục '{remote_path}': {str(e)}")

