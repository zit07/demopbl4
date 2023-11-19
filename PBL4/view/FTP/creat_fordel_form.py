import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import messagebox, ttk
from controller.FTP_controller import FTPController
import os
from view.general_method import CREATICONBUTTON

class CreatFolderForm(tk.Toplevel):
    def __init__(self, parent, main_form, remote_folder_path):
        super().__init__(parent)
        self.main_form = main_form
        self.remote_folder_path = remote_folder_path 
        self.title("Tạo thư mục mới")

        # Tạo label hiển thị đường dẫn tệp đã chọn
        self.file_label = tk.Label(self, text='Chú ý: tên thư mục không chứa dấu "."', fg='yellow')
        self.file_label.pack(pady=(40, 10))
    
        self.noti_label = tk.Label(self)
        self.noti_label.pack()
        
        main_frame = tk.Frame(self)
        main_frame.pack()
        
        sub_frame1 = ttk.Frame(main_frame)
        sub_frame1.pack(side=tk.TOP, padx=30, pady=10)
        label = ttk.Label(sub_frame1, text="Nhập tên cho thư mục mới:")
        label.pack(side=tk.TOP)
        self.folder_name_entry = tk.Entry(sub_frame1, width=30)
        self.folder_name_entry.pack(side=tk.TOP, pady=10)
        self.folder_name_entry.insert(0, "") 
        
        sub_frame2 = ttk.Frame(main_frame)
        sub_frame2.pack(side=tk.BOTTOM, padx=30, pady=20)
        ttk.Label(sub_frame2, text="").pack(side=tk.LEFT, expand=True)
        self.exit_icon, self.exit_label = CREATICONBUTTON(self, sub_frame2, "quit.png", "Thoát", 12, self.destroy)
        self.download_icon, self.tftp_label = CREATICONBUTTON(self, sub_frame2, "confirm.png", "Xác nhận", 12, self.creat_folder)
        ttk.Label(sub_frame2, text="").pack(side=tk.LEFT, expand=True)

    def creat_folder(self):
        if self.remote_folder_path:
            folder_name = self.folder_name_entry.get()
            if not folder_name:
                self.noti_label.config(text='Vui lòng nhập tên cho folder mới', fg='red')
                return
            elif "." in folder_name:
                self.noti_label.config(text='Tên thư mục không được chứa dấu "."', fg='red')
                return
            else:
                self.remote_folder_path = os.path.join(self.remote_folder_path, folder_name)
                creat, list_files_in_directory, output = FTPController().creat_folder(self.remote_folder_path)
                if creat:
                    self.destroy()
                    self.main_form.build_folder_tree(list_files_in_directory, "", "/", True)  
                else:
                    self.noti_label.config(text=output, fg='red')

