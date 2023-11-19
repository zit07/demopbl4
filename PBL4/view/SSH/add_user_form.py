import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk
from controller.SSH_controller import SSHController
from view.general_method import CREATICONBUTTON
import re

class AddUserForm(tk.Toplevel):
    def __init__(self, parent, main_form):
        super().__init__(parent)
        self.main_form = main_form
        self.title("Tạo người dùng mới")
        
        self.attention_label = tk.Label(self, text='Chú ý: mật khẩu phải có ít nhất 8 ký tự gồm chữ và số', fg='yellow')
        self.attention_label.pack(pady=(20, 10))
        
        self.noti_label = tk.Label(self)
        self.noti_label.pack(pady=(10))
        
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        form_label_input = ttk.Frame(main_frame)
        form_label_input.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.new_username_label = tk.Label(form_label_input, text="Tên đăng nhập:")
        self.new_username_label.grid(row=0, column=0, sticky="w")
        self.new_username_entry = tk.Entry(form_label_input)
        self.new_username_entry.grid(row=0, column=1, padx=10, sticky="ew")

        self.password_label = tk.Label(form_label_input, text="Mật khẩu:")
        self.password_label.grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(form_label_input)
        self.password_entry.grid(row=1, column=1, padx=10, sticky="ew")
        
        self.password_root_label = tk.Label(form_label_input, text="Mật khẩu của bạn:")
        self.password_root_label.grid(row=2, column=0, sticky="w")
        self.password_root_entry = tk.Entry(form_label_input, show="*")
        self.password_root_entry.grid(row=2, column=1, padx=10, sticky="ew")

        sub_frame1 = ttk.Frame(main_frame)
        sub_frame1.grid(row=3, column=0, padx=30, pady=20, sticky="nsew")
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)
        self.exit_icon, self.exit_label = CREATICONBUTTON(self, sub_frame1, "quit.png", "Thoát", 12, self.destroy)
        self.download_icon, self.tftp_label = CREATICONBUTTON(self, sub_frame1, "confirm.png", "Xác nhận", 12, self.creat_new_user)
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)

    
    def creat_new_user(self):
        new_username = self.new_username_entry.get()
        password = self.password_entry.get()
        password_root = self.password_root_entry.get()
        
        if not new_username:
            self.noti_label.config(text="Nhập tên đăng nhập cho người dùng mới!", fg='red')
            return
        elif not password or len(password) < 8 or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password):
            self.noti_label.config(text="Kiểm tra lại mật khẩu!", fg='red')
            return
        elif not password_root:
            self.noti_label.config(text="Nhập mật khẩu của bạn!", fg='red')
            return
        else:
            creat, output = SSHController().creat_user(new_username, password, password_root)
            if creat:
                self.main_form.execute_command("", output)
                self.destroy()
            else:
                self.noti_label.config(text=output, fg='red')
            