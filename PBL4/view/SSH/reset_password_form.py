import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk
from controller.SSH_controller import SSHController
from view.general_method import CREATICONBUTTON

class ResetPassword(tk.Toplevel):
    def __init__(self, parent, main_form):
        super().__init__(parent)
        self.main_form = main_form
        self.title("Reset mật khẩu cho người dùng")
        
        self.attention_label = tk.Label(self, text='Chú ý: mật khẩu phải có ít nhất 8 ký tự gồm chữ và số', fg='yellow')
        self.attention_label.pack(pady=(10, 10))
        
        self.noti_label = tk.Label(self)
        self.noti_label.pack(pady=(10))
        
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        form_label_input = ttk.Frame(main_frame)
        form_label_input.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.username_label = tk.Label(form_label_input, text="Tên đăng nhập:")
        self.username_label.grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(form_label_input)
        self.username_entry.grid(row=0, column=1, padx=10, sticky="ew")

        self.new_password_label = tk.Label(form_label_input, text="Mật khẩu mới:")
        self.new_password_label.grid(row=1, column=0, sticky="w")
        self.new_password_entry = tk.Entry(form_label_input)
        self.new_password_entry.grid(row=1, column=1, padx=10, sticky="ew")
        
        self.password_root_label = tk.Label(form_label_input, text="Mật khẩu của bạn:")
        self.password_root_label.grid(row=2, column=0, sticky="w")
        self.password_root_entry = tk.Entry(form_label_input, show="*")
        self.password_root_entry.grid(row=2, column=1, padx=10, sticky="ew")

        sub_frame1 = ttk.Frame(main_frame)
        sub_frame1.grid(row=3, column=0, padx=30, pady=20, sticky="nsew")
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)
        self.exit_icon, self.exit_label = CREATICONBUTTON(self, sub_frame1, "quit.png", "Thoát", 12, self.destroy)
        self.download_icon, self.tftp_label = CREATICONBUTTON(self, sub_frame1, "confirm.png", "Xác nhận", 12, self.reset_password)
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)

    
    def reset_password(self):
        username = self.username_entry.get()
        new_password = self.new_password_entry.get()
        password_root = self.password_root_entry.get()
        
        if not username:
            self.noti_label.config(text="Vui lòng nhập tên đăng nhập cần reset mật khẩu!", fg='red')
            return
        elif not new_password or len(new_password) < 8:
            self.noti_label.config(text="Vui lòng kiểm tra lại mật khẩu!", fg='red')
            return
        elif not password_root:
            self.noti_label.config(text="Vui lòng nhập mật khẩu của bạn!", fg='red')
            return
        else:
            reset, output = SSHController().reset_password(password_root, username, new_password)
            if reset:
                self.main_form.execute_command("", output)
                self.destroy()
            else:
                self.noti_label.config(text=output, fg='red')
