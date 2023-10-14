import tftpy

# Địa chỉ IP của máy chủ TFTP
server_ip = '192.168.64.10'

# Tên tệp trên máy chủ TFTP
remote_file_name = 'ACL.pdf'

# Đường dẫn đến thư mục đích cho việc tải xuống
local_dir_path = '/Users/haison/Downloads/'

# Tạo một đối tượng TftpClient
client = tftpy.TftpClient(server_ip)

try:
    # Tải xuống tệp từ máy chủ TFTP và lưu vào thư mục đích
    client.download(remote_file_name, local_dir_path + remote_file_name)
    print(f"Tải xuống {remote_file_name} thành công và lưu vào {local_dir_path}.")
except Exception as e:
    print(f"Lỗi khi tải xuống từ máy chủ TFTP: {e}")
