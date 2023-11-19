import socket

class FTPHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.recv_response()
            return True, ""
        except Exception as e:
            print(str(e))
            return False, "Không thể kết nối đến máy chủ"
        
    def send_command(self, command):
        self.sock.sendall(command.encode() + b'\r\n')

    def recv_response(self):
        data = b''
        while True:
            part = self.sock.recv(4096)
            data += part
            if b'\r\n' in part:
                break
        return data

    def login(self, username, password):
        try:
            self.send_command('USER ' + username)
            response = self.recv_response()
            if response.startswith(b'331'):
                self.send_command('PASS ' + password)
                response = self.recv_response()
                if response.startswith(b'230'):
                    return True, ""
                else:
                    return False, "Sai tài khoản hoặc mật khẩu"
            else:
                return False, "Hiện tại máy chủ đang bận"
        except Exception as e:
            print(f"Lỗi khi đăng nhập: {e}")
            return False, ""

    def get_list_files_in_directory(self, remote_directory):
        self.send_command('CWD ' + remote_directory)
        response = self.recv_response()
        if not response.startswith(b'250'):
            return []

        self.send_command('PASV')
        response = self.recv_response()
        if not response.startswith(b'227'):
            return []

        # Phân tích phản hồi PASV để lấy địa chỉ và cổng kết nối dữ liệu
        start = response.find(b'(') + 1
        end = response.find(b')', start)
        address_parts = response[start:end].split(b',')
        data_host = '.'.join(part.decode() for part in address_parts[:4])
        data_port = (int(address_parts[4]) << 8) + int(address_parts[5])

        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.connect((data_host, data_port))
        
        self.send_command('LIST')
        response = self.recv_response()
        if not response.startswith(b'150'):
            return []

        data = b''
        while True:
            part = data_sock.recv(4096)
            if not part:
                break
            data += part
        data_sock.close()
        response = self.recv_response()  # Nhận phản hồi 226 Transfer Complete
        
        return data.decode().split('\n')
    
    def storbinary(self, cmd, file):
        """Gửi file dưới dạng nhị phân tới máy chủ FTP.

        Args:
            cmd (str): Lệnh FTP, ví dụ: 'STOR filename.txt'
            file: Đối tượng file mở ở chế độ nhị phân ('rb')
        """
        try:
            self.send_command('TYPE I')  # Chuyển sang chế độ truyền nhị phân
            self.recv_response()

            # Mở kết nối dữ liệu thông qua chế độ PASV
            self.send_command('PASV')
            response = self.recv_response()
            if not response.startswith(b'227'):
                raise Exception("Không thể chuyển sang chế độ PASV")

            # Phân tích địa chỉ và cổng từ phản hồi PASV
            start = response.find(b'(') + 1
            end = response.find(b')', start)
            address_parts = response[start:end].split(b',')
            data_host = '.'.join(part.decode() for part in address_parts[:4])
            data_port = (int(address_parts[4]) << 8) + int(address_parts[5])

            # Kết nối tới máy chủ dữ liệu
            data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_sock.connect((data_host, data_port))

            # Gửi lệnh STOR
            self.send_command("STOR " + cmd)
            response = self.recv_response()
            if not response.startswith(b'150'):
                raise Exception("Không thể bắt đầu tải lên")

            # Đọc và gửi dữ liệu file
            while True:
                data = file.read(4096)
                if not data:
                    break
                data_sock.sendall(data)

            data_sock.close()
            response = self.recv_response()  # Nhận phản hồi 226 Transfer Complete
            return response.startswith(b'226'), ""
        except Exception as e:
            return False, f"Lỗi: {e}"
    
    def retrbinary(self, cmd, callback):
        """Nhận file dưới dạng nhị phân từ máy chủ FTP.

        Args:
            cmd (str): Lệnh FTP, ví dụ: 'RETR filename.txt'
            callback: Hàm callback được gọi với mỗi khối dữ liệu nhận được
        """
        try:
            self.send_command('TYPE I')  # Chuyển sang chế độ truyền nhị phân
            self.recv_response()

            # Mở kết nối dữ liệu thông qua chế độ PASV
            self.send_command('PASV')
            response = self.recv_response()
            if not response.startswith(b'227'):
                raise Exception("Không thể chuyển sang chế độ PASV")

            # Phân tích địa chỉ và cổng từ phản hồi PASV
            start = response.find(b'(') + 1
            end = response.find(b')', start)
            address_parts = response[start:end].split(b',')
            data_host = '.'.join(part.decode() for part in address_parts[:4])
            data_port = (int(address_parts[4]) << 8) + int(address_parts[5])

            # Kết nối tới máy chủ dữ liệu
            data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_sock.connect((data_host, data_port))

            # Gửi lệnh RETR
            self.send_command("RETR " + cmd)
            response = self.recv_response()
            if not response.startswith(b'150'):
                raise Exception("Không thể bắt đầu tải xuống")

            # Nhận và xử lý dữ liệu
            while True:
                data = data_sock.recv(4096)
                if not data:
                    break
                callback(data)

            data_sock.close()
            response = self.recv_response()  # Nhận phản hồi 226 Transfer Complete
            return response.startswith(b'226'), ""
        except Exception as e:
            return False, f"Lỗi: {e}"
        
    def mkd(self, remote_directory):
        """Tạo một thư mục mới trên máy chủ FTP.

        Args:
            remote_directory (str): Đường dẫn của thư mục mới cần tạo
        """
        try:
            self.send_command('MKD ' + remote_directory)
            response = self.recv_response()
            if response.startswith(b'257'):
                return True, ""
            else:
                print(f"Không thể tạo thư mục '{remote_directory}'. Phản hồi: {response.decode()}")
                return False, f"Không thể tạo thư mục '{remote_directory}'. Phản hồi: {response.decode()}"
        except Exception as e:
            return False, f"Lỗi: {e}"
        
    def rename(self, remote_old_path, remote_new_path):
        """Đổi tên file hoặc thư mục trên máy chủ FTP.

        Args:
            remote_old_path (str): Đường dẫn cũ của file hoặc thư mục.
            remote_new_path (str): Đường dẫn mới của file hoặc thư mục.
        """
        try:
            # Gửi lệnh RNFR với đường dẫn cũ
            self.send_command('RNFR ' + remote_old_path)
            response = self.recv_response()
            if not response.startswith(b'350'):
                print(f"Không thể chuẩn bị đổi tên từ '{remote_old_path}'. Phản hồi: {response.decode()}")
                return False, f"Không thể chuẩn bị đổi tên từ '{remote_old_path}'. Phản hồi: {response.decode()}"

            # Gửi lệnh RNTO với đường dẫn mới
            self.send_command('RNTO ' + remote_new_path)
            response = self.recv_response()
            if response.startswith(b'250'):
                return True, ""
            else:
                print(f"Không thể đổi tên đến '{remote_new_path}'. Phản hồi: {response.decode()}")
                return False, f"Không thể đổi tên thành '{remote_new_path}'. Phản hồi: {response.decode()}"
        except Exception as e:
            return False, f"Lỗi: {e}"
        
    def delete(self, remote_path):
        """Xóa một tệp tin trên máy chủ FTP.

        Args:
            remote_path (str): Đường dẫn của tệp tin cần xóa.
        """
        try:
            self.send_command('DELE ' + remote_path)
            response = self.recv_response()
            if response.startswith(b'250'):
                return True, ""
            else:
                print(f"Không thể xóa tệp '{remote_path}'. Phản hồi: {response.decode()}")
                return False, f"Xoá thất bại, lỗi: {response.decode()}"
        except Exception as e:
            return False, f"Xoá thất bại, lỗi: {e}"
        
    def rmd(self, remote_path):
        """Xóa một thư mục trên máy chủ FTP.

        Args:
            remote_path (str): Đường dẫn của thư mục cần xóa.
        """
        self.send_command('RMD ' + remote_path)
        response = self.recv_response()
        if response.startswith(b'250'):
            return True
        else:
            print(f"Không thể xóa thư mục '{remote_path}'. Phản hồi: {response.decode()}")
            return False
        
    def change_directory(self, remote_path):
        """Thay đổi thư mục làm việc trên máy chủ FTP và kiểm tra xem đó có phải là thư mục.

        Args:
            remote_path (str): Đường dẫn của thư mục cần chuyển đến.

        Returns:
            bool: Trả về True nếu thành công, ngược lại False.
        """
        self.send_command('CWD ' + remote_path)
        response = self.recv_response()
        if response.startswith(b'250'):
            return True
        else:
            print(f"Không thể chuyển đến thư mục '{remote_path}'. Phản hồi: {response.decode()}")
            return False
    
    def quit(self):
        self.send_command('QUIT')
        self.recv_response()
        self.sock.close()
