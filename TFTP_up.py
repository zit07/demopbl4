import tftpy

# Địa chỉ IP của máy chủ TFTP
server_ip = '192.168.64.10'

# Đường dẫn đến tệp cần tải lên
local_file_path = '/Users/haison/Downloads/ACL456.pdf'

# Tên tệp trên máy chủ TFTP
remote_file_name = 'ACL.pdf'

# Tạo một đối tượng TftpClient
client = tftpy.TftpClient(server_ip)

try:
    # Tải lên tệp lên máy chủ TFTP
    client.upload(remote_file_name, local_file_path)
    print(f"Tải lên {local_file_path} lên máy chủ TFTP thành công.")
except Exception as e:
    print(f"Lỗi khi tải lên máy chủ TFTP: {e}")
