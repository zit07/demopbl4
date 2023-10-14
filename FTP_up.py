# ftp_server = "192.168.64.10"
# username = "ftpuser"
# password = "ahihi123"
# remote_path = "/Users/haison/Downloads/ACL456.pdf"

from ftplib import FTP

# Thông tin máy chủ FTP
ftp_host = "192.168.64.10"
ftp_port = 21
ftp_username = "ftpuser"
ftp_password = "ahihi123"  

# Đường dẫn đến tệp PDF cần tải lên
local_pdf_path = "/Users/haison/Downloads/ACL456.pdf"  # Đường dẫn đến tệp PDF trên máy tính của bạn
remote_pdf_directory = "/upload/"  # Đường dẫn đến thư mục "upload" trên máy chủ FTP
remote_pdf_filename = "file.pdf"  # Tên tệp PDF trên máy chủ FTP

# Tạo kết nối FTP
ftp = FTP()
ftp.connect(ftp_host, ftp_port)
ftp.login(ftp_username, ftp_password)

# Định dạng đường dẫn đến thư mục và tên tệp PDF trên máy chủ FTP
remote_pdf_path = remote_pdf_directory + remote_pdf_filename

# Mở tệp PDF cục bộ và tải lên máy chủ FTP
with open(local_pdf_path, 'rb') as local_file:
    ftp.storbinary('STOR ' + remote_pdf_path, local_file)

# Đóng kết nối FTP
ftp.quit()

print("Tải tệp PDF lên máy chủ FTP thành công.")
