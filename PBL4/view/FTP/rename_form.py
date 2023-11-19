import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk
from controller.FTP_controller import FTPController
import os
from view.general_method import CREATICONBUTTON

class RenameForm(tk.Toplevel):
    def __init__(self, parent, main_form, remote_old_path):
        super().__init__(parent)
        self.main_form = main_form
        self.remote_old_path = remote_old_path 
        self.title("Đổi tên")

        self.noti_label = tk.Label(self)
        self.noti_label.pack(pady=(20,0))
        
        form_frame = ttk.Frame(self)
        form_frame.pack(fill=tk.BOTH, pady=(20,0), expand=True)
        
        sub_frame1 = ttk.Frame(form_frame)
        sub_frame1.pack(side=tk.TOP, padx=(20))
        self.filename_label = tk.Label(sub_frame1, text="Nhập tên mới:")
        self.filename_label.pack(side=tk.LEFT, pady=10)
        self.folder_name_entry = tk.Entry(sub_frame1, width=30)
        self.folder_name_entry.pack(side=tk.LEFT, pady=10)
        self.folder_name_entry.insert(0, remote_old_path.split("/")[-1])

        sub_frame2 = ttk.Frame(form_frame)
        sub_frame2.pack(side=tk.BOTTOM, pady=(20))
        ttk.Label(sub_frame2, text="").pack(side=tk.LEFT, expand=True)
        self.quit_icon, self.quit_label = CREATICONBUTTON(self, sub_frame2, "quit.png", "Thoát", 12, self.destroy)
        self.confirm_icon, self.confirm_label = CREATICONBUTTON(self, sub_frame2, "confirm.png", "Xác nhận", 12, self.rename)
        ttk.Label(sub_frame2, text="").pack(side=tk.LEFT, expand=True)


    def rename(self):
        if self.remote_old_path:
            new_name = self.folder_name_entry.get()
            if not new_name:
                self.noti_label.config(text="Tên mới không được để trống!", fg='red')
                return
            elif "." in self.remote_old_path and not "." in new_name:
                self.noti_label.config(text="Tên mới thiếu kiểu tệp tin (.txt, .pdf...)!", fg='red')
                return
            # Tách thành phần thư mục và tệp ra khỏi đường dẫn
            # Lấy tất cả phần tử trừ phần cuối cùng (tệp)
            # Kết hợp đường dẫn và tên moi để tạo đường dẫn moi
            remote_new_path = os.path.join("/".join(self.remote_old_path.split("/")[:-1]), new_name)
            creat, list_files_in_directory, output = FTPController().rename(self.remote_old_path, remote_new_path)
            if creat:
                self.destroy()
                self.main_form.build_folder_tree(list_files_in_directory, "", "/", True)  
            else:
                self.noti_label.config(text=output, fg='red')
