import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk
from controller.SSH_controller import SSHController
from view.general_method import CREATICONBUTTON
from view.general_method import is_strong_password

class ChangePassword(tk.Toplevel):
    def __init__(self, parent, main_form):
        super().__init__(parent)
        self.main_form = main_form
        self.title("Tạo người dùng mới")
        
        # self.file_label = tk.Label(self, text='Chú ý: mật khẩu phải có ít nhất 8 ký tự gồm chữ và số', fg='yellow')
        # self.file_label.pack(pady=(40, 10))
        
        self.noti_label = tk.Label(self)
        self.noti_label.pack(pady=(20,0))
        
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        form_label_input = ttk.Frame(main_frame)
        form_label_input.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.old_password_label = tk.Label(form_label_input, text="Mật khẩu cũ:")
        self.old_password_label.grid(row=0, column=0, sticky="w")
        self.old_password_entry = tk.Entry(form_label_input, show="*")
        self.old_password_entry.grid(row=0, column=1, padx=10, sticky="ew")

        self.new_pass_label = tk.Label(form_label_input, text="Mật khẩu mới:")
        self.new_pass_label.grid(row=1, column=0, sticky="w")
        self.new_pass_entry = tk.Entry(form_label_input, show="*")
        self.new_pass_entry.grid(row=1, column=1, padx=10, sticky="ew")
        
        self.confirm_newpass_label = tk.Label(form_label_input, text="Xác nhận mật khẩu mới:")
        self.confirm_newpass_label.grid(row=2, column=0, sticky="w")
        self.confirm_newpass_entry = tk.Entry(form_label_input, show="*")
        self.confirm_newpass_entry.grid(row=2, column=1, padx=10, sticky="ew")

        sub_frame1 = ttk.Frame(main_frame)
        sub_frame1.grid(row=3, column=0, padx=30, pady=20, sticky="nsew")
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)
        self.exit_icon, self.exit_label = CREATICONBUTTON(self, sub_frame1, "quit.png", "Thoát", 12, self.destroy)
        self.download_icon, self.tftp_label = CREATICONBUTTON(self, sub_frame1, "confirm.png", "Xác nhận", 12, self.change_password)
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)

    
    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_pass_entry.get()
        confirm_newpass = self.confirm_newpass_entry.get()
        
        if not old_password:
            self.noti_label.config(text="Vui lòng nhập mật khẩu cũ!", fg='red')
            return
        elif not new_password or len(new_password) < 8:
            self.noti_label.config(text="Mật khẩu phải có ít nhất 8 ký tự gồm chữ và số!", fg='red')
            return
        elif confirm_newpass != new_password:
            self.noti_label.config(text="Mật khẩu mới và xác nhận mật khẩu mới không giống nhau!", fg='red')
            return
        else:
            strong_pass, err = is_strong_password(new_password)
            if strong_pass:
                changepassword, output = SSHController().change_password(old_password, new_password)
                if changepassword:
                    self.main_form.execute_command("", output)
                    self.destroy()
                else:
                    self.noti_label.config(text=output, fg='red')
            else:
                self.noti_label.config(text=err, fg='red')
