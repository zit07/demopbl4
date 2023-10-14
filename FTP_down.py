from ftplib import FTP

# Thông tin máy chủ FTP
ftp_host = "192.168.64.10"
ftp_port = 21
ftp_username = "ftpuser"
ftp_password = "ahihi123"  # Thay thế bằng mật khẩu FTP của bạn

# Tên tệp bạn vừa mới tải lên
remote_pdf_directory = "/upload/"  # Đường dẫn đến thư mục "upload" trên máy chủ FTP
remote_pdf_filename = "file.pdf"  # Tên tệp PDF trên máy chủ FTP

# Tạo kết nối FTP
ftp = FTP()
ftp.connect(ftp_host, ftp_port)
ftp.login(ftp_username, ftp_password)

# Định dạng đường dẫn đến tệp PDF trên máy chủ FTP
remote_pdf_path = remote_pdf_directory + remote_pdf_filename

# Tạo tên tệp cục bộ để lưu tệp PDF tải về
local_pdf_filename = "downloaded_file.pdf"

# Tải tệp PDF về máy tính cục bộ
with open(local_pdf_filename, 'wb') as local_file:
    ftp.retrbinary('RETR ' + remote_pdf_path, local_file.write)

# Đóng kết nối FTP
ftp.quit()

print(f"Tải tệp {remote_pdf_filename} về máy tính thành công.")