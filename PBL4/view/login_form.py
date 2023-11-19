import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk, PhotoImage
from controller.FTP_controller import FTPController
from controller.SSH_controller import SSHController
from model.global_resources import directoryIMG

class LoginForm(tk.Toplevel):
    def __init__(self, parent, main_form, method):
        super().__init__(parent)
        self.main_form = main_form
        self.method = method
        self.title("Đăng nhập " + method)
        self.tree_folder_form = None
        self.transient(parent)
        
        # Tạo một frame để chứa các thành phần
        form_frame = ttk.Frame(self)
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        login_icon = PhotoImage(file=directoryIMG + "login" + self.method + ".png").subsample(6, 6)
        self.icon_label = tk.Label(form_frame, image=login_icon)
        self.icon_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10), padx=(10))
        self.login_icon = login_icon
        
        # Tạo label hiển thị thong bao
        self.noti_label = tk.Label(form_frame)
        
        self.username_label = tk.Label(form_frame, text="Tên đăng nhập:")
        self.username_label.grid(row=2, column=0, sticky="w")

        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=2, column=1, padx=10, sticky="ew")

        self.password_label = tk.Label(form_frame, text="Mật khẩu:")
        self.password_label.grid(row=3, column=0, sticky="w")

        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, sticky="ew")
        
        style = ttk.Style()
        style.configure("LoginButton.TButton", relief="ridge", borderwidth=5, padding=10, background="lightgray", font=("Arial", 12))
        self.login_button_style = ttk.Button(form_frame, text="Đăng nhập", command=self.login, style="LoginButton.TButton")
        self.login_button_style.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get().replace(" ", "")
        password = self.password_entry.get().replace(" ", "")

        if username and password:
            success = None
            list_files_in_directory = None
            error_login = ""
            checkroot = None
            if self.method == "FTP":
                success, list_files_in_directory, error_login = FTPController().login_ftp(username, password)
            else:
                success, checkroot = SSHController().login_ssh(username, password)

            if success:
                if self.method == "FTP":
                    self.main_form.show_tree_folder_form(list_files_in_directory)
                else:
                    self.main_form.show_ssh_form(checkroot)
                self.destroy()
            else:
                self.noti_label.config(text=error_login, fg='red')
                self.noti_label.grid(row=1, column=0, columnspan=2, pady=10)
        else:
            if username:
                self.noti_label.config(text="Vui lòng điền mật khẩu!", fg='red')
            else:
                self.noti_label.config(text="Vui lòng điền tên đăng nhập!", fg='red')
            self.noti_label.grid(row=1, column=0, columnspan=2, pady=10)
