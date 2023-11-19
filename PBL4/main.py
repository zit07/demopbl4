import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from view.login_form import LoginForm
from view.center_windown import center_window 
from view.FTP.tree_folder_form import TreeFolderForm
from view.TFTP.main_form_TFTP import MainFormTFTP
from view.SSH.ssh_mainform import MainFormSSH
from controller.FTP_controller import FTPController
from controller.SSH_controller import SSHController
from model.global_resources import x, y
from view.general_method import CREATICONBUTTON

class MainForm:
    def show_tree_folder_form(self, list_files_in_directory):
        self.tree_folder_form = TreeFolderForm(self.root, list_files_in_directory)
        center_window(self.tree_folder_form, x, y)
        self.tree_folder_form.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.withdraw()

    def show_ssh_form(self, root):
        self.ssh_form = MainFormSSH(self.root, root)
        center_window(self.ssh_form, x, y)
        self.ssh_form.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.withdraw()
        
    def on_closing(self):
        FTPController().logout_ftp()
        SSHController().logout_ssh()
        if hasattr(self, 'main_form_tftp'):
            try:
                self.main_form_tftp.destroy()
            except:
                print()
        self.root.destroy()

    def __init__(self, root):
        self.root = root
        self.root.title("Chọn giao thức")

        # Tạo một hộp chứa nút
        icon_frame = tk.Frame(root)
        icon_frame.pack(pady=200)  # Thêm khoảng cách 200 pixels từ trên xuống

        self.ftp_icon, self.ftp_label = CREATICONBUTTON(self, icon_frame, "ftp.png", "FTP", 5, lambda: self.show_login_form("FTP"))
        self.tftp_icon, self.tftp_label = CREATICONBUTTON(self, icon_frame, "tftp.png", "TFTP", 5, self.show_main_form_tftp)
        self.ssh_icon, self.ssh_label = CREATICONBUTTON(self, icon_frame, "ssh.png", "SSH", 5, lambda: self.show_login_form("SSH"))
        
    def show_login_form(self, giaothuc):
        login_form = LoginForm(self.root, self, giaothuc)
        center_window(login_form, 350, 300)
        login_form.mainloop()    
        
    def show_main_form_tftp(self):
        self.main_form_tftp = MainFormTFTP(self.root)
        center_window(self.main_form_tftp, x, y)
        self.root.withdraw()  # Ẩn cửa sổ gốc
        self.main_form_tftp.protocol("WM_DELETE_WINDOW", self.on_closing) 
        self.main_form_tftp.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainForm(root)
    center_window(root, x, y)
    root.mainloop()