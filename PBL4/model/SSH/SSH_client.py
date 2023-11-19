import re
import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import paramiko
from model.global_resources import ssh
from model.global_resources import host
from model.global_resources import portSSH

class SSHHandler:
    def connect_ssh(self, username, password):
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, portSSH, username, password)
            return True
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials.")
            return False
        except paramiko.SSHException as sshException:
            print(f"Could not establish SSH connection: {sshException}")
            return False
        except Exception as e:
            print(str(e)) 
            return False

    def disconnect(self):
        if ssh is not None:
            ssh.close()
            print("SSH connection closed.")
    
    def execute_ssh_command(self, command):
        try:
            # Kiểm tra nếu client đã được khởi tạo và transport là hoạt động
            if ssh.get_transport() is None :
                return "SSH Client không được kết nối."
            
            # Thực thi lệnh qua SSH
            stdin, stdout, stderr = ssh.exec_command(command)
            stdin.write('password\n')
            stdin.flush()
            # Đọc đầu ra từ lệnh
            stdout_output = stdout.read()
            stderr_output = stderr.read()
            
            # Kiểm tra và trả về đầu ra hoặc lỗi
            if stdout_output:
                return stdout_output.decode('utf-8')
            elif stderr_output:
                return stderr_output.decode('utf-8')
            return "Lệnh không có đầu ra."
        except Exception as e:
            return f"Lỗi khi thực thi lệnh: {str(e)}"
    
    def create_user(self, new_username, password, password_root):
        try:
            # Tạo người dùng mà không cần mật khẩu ban đầu
            create_user_command = f'echo {password_root} | sudo -S adduser {new_username} --gecos "" --disabled-password'
            stdin, stdout, stderr = ssh.exec_command(create_user_command)
            stdin.flush()
            
            stderr_string = ''.join(stderr.read().decode().split('\n')).replace(" ", "").lower()
            if "passwordforson:sorry,tryagain" in stderr_string:
                return False, "Mật khẩu của bạn không chính xác"
            if "theuser" in stderr_string and "alreadyexists." in stderr_string:
                return False, "Tên đăng nhập đã tồn tại"
            
            # Đặt mật khẩu cho người dùng
            set_password = self.reset_password(password_root, new_username, password)
            if not set_password: return False, "Mật khẩu không đủ bảo mật"
            
            commands = [
                    f'echo {password_root} | sudo -S mkdir /home/{new_username}/ftp',
                    f'echo {password_root} | sudo -S chown nobody:nogroup /home/{new_username}/ftp',
                    f'echo {password_root} | sudo -S chmod a-w /home/{new_username}/ftp',
                    f'echo {password_root} | sudo -S mkdir /home/{new_username}/ftp/home',
                    f'echo {password_root} | sudo -S chown {new_username}:{new_username} /home/{new_username}/ftp/home'
                ]

            # Thực hiện từng lệnh để tạo thư mục home ftp
            for command in commands:
                stdin, stdout, stderr = ssh.exec_command(command)
                if stdout.channel.recv_exit_status() != 0:
                    return False, f"Lỗi: {stderr.read().decode()}"
                    
            return True, f"Thêm người dùng {new_username} thành công, mật khẩu là {password}"
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
    
    def delete_user(self, username, rootpassword):
        try:
            command = f'echo {rootpassword} | sudo -S userdel -r {username}'
            stdin, stdout, stderr = ssh.exec_command(command)
            
            stderr_string = ''.join(stderr.read().decode().split('\n')).replace(" ", "").lower()
            if "passwordforson:sorry,tryagain" in stderr_string:
                return False, "Mật khẩu của bạn không chính xác"
            if "user" in stderr_string and "doesnotexist" in stderr_string:
                return False, f"Người dùng {username} không tồn tại"
            
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                return True, f"Xoá người dùng {username} thành công"
            
            return False, f"Xoá người dùng {username} thất bại"
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False, f"An error occurred: {str(e)}"
    
    def change_password(self, old_password, new_password):
        try:
            set_password_command = f'echo -e "{old_password}\n{new_password}\n{new_password}" | passwd'
            stdin, stdout, stderr = ssh.exec_command(set_password_command)
            stdin.flush()
            
            stderr_string = ''.join(stderr.read().decode().split('\n')).replace(" ", "").lower()
            if "currentpassword:currentpassword:" in stderr_string:
                return False, "Mật khẩu của bạn không chính xác"
            
            if stdout.channel.recv_exit_status() != 0: 
                return False, "Mật khẩu mới chưa đủ bảo mật, hãy thử lại"
            else:
                return True, f"Thay đổi mật khẩu thành công, mật khẩu mới là {new_password}"
        except Exception as e:
            return False, f"Lỗi: {e}"

    def reset_password(self, password_root, username, new_password):
        try:
            set_password_command = f'echo -e "{password_root}\n{new_password}\n{new_password}" | sudo -S passwd {username}'
            stdin, stdout, stderr = ssh.exec_command(set_password_command)
            stdin.flush()
            stderr_string = ''.join(stderr.read().decode().split('\n')).replace(" ", "").lower()
            if "passwordforson:sorry,tryagain" in stderr_string:
                return False, "Mật khẩu của bạn không chính xác"
            
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                return True, f"Reset mật khẩu cho người dùng {username} thành công, mật khẩu mới là {new_password}"
            
            return False, f"Mật khẩu mới kém bảo mật, hãy thử lại"
        
        except Exception as e:
            return False, f"Lỗi: {e}"