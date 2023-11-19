import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk
from controller.SSH_controller import SSHController
from view.general_method import CREATICONBUTTON

class DeleteUser(tk.Toplevel):
    def __init__(self, parent, main_form):
        super().__init__(parent)
        self.main_form = main_form
        self.title("Xoá người dùng")

        self.attention_label = tk.Label(self, text='Chú ý: Người dùng đã xoá không thể khôi phục!', fg='yellow')
        self.attention_label.pack(pady=(20, 10))
        
        self.noti_label = tk.Label(self)
        self.noti_label.pack(pady=(20,0))
        
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        form_label_input = ttk.Frame(main_frame)
        form_label_input.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.username_label = tk.Label(form_label_input, text="Tên người dùng muốn xoá:")
        self.username_label.grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(form_label_input)
        self.username_entry.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.password_root_label = tk.Label(form_label_input, text="Mật khẩu của bạn:")
        self.password_root_label.grid(row=1, column=0, sticky="w")
        self.password_root_entry = tk.Entry(form_label_input, show="*")
        self.password_root_entry.grid(row=1, column=1, padx=10, sticky="ew")

        sub_frame1 = ttk.Frame(main_frame)
        sub_frame1.grid(row=2, column=0, padx=30, pady=20, sticky="nsew")
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)
        self.exit_icon, self.exit_label = CREATICONBUTTON(self, sub_frame1, "quit.png", "Thoát", 12, self.destroy)
        self.download_icon, self.tftp_label = CREATICONBUTTON(self, sub_frame1, "confirm.png", "Xác nhận", 12, self.delete_user)
        ttk.Label(sub_frame1, text="").pack(side=tk.LEFT, expand=True)


    def delete_user(self):
        username = self.username_entry.get()
        password_root = self.password_root_entry.get()
        
        if not username:
            self.noti_label.config(text="Vui lòng nhập tên người dùng muốn xoá!", fg='red')
            return
        elif not password_root:
            self.noti_label.config(text="Vui lòng nhập mật khẩu của bạn!", fg='red')
            return
        else:
            delete, output = SSHController().delete_user(username, password_root)
            if delete:
                self.main_form.execute_command("", output)
                self.destroy()
            else:
                self.noti_label.config(text=output, fg='red')
