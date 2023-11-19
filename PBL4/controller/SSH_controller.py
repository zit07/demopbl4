import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

from model.ssh_handler import SSHHandler
from model.global_resources import UsernameSSH
from model.global_resources import UsernameSSH_Root

class SSHController:
    def login_ssh(self, username, password):
        UsernameSSH().set_username(username)
        root = True if username == UsernameSSH_Root().get_username_root() else False
        return SSHHandler().connect_ssh(username, password), root
    
    def logout_ssh(self):
        SSHHandler().disconnect()
    
    def execute_ssh(self, command):
        return SSHHandler().execute_ssh_command(command)
    
    def creat_user(self, new_username, paddword, password_root):
        return SSHHandler().create_user(new_username, paddword, password_root)
    
    def delete_user(self, username, password_root):
        return SSHHandler().delete_user(username, password_root)

    def change_password(self, oldpassword, newpassword):
        return SSHHandler().change_password(oldpassword, newpassword)
    
    def reset_password(self, root_password, username, newpassword):
        return SSHHandler().reset_password(root_password, username, newpassword)
