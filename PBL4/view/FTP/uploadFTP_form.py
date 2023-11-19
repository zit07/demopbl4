import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from controller.FTP_controller import FTPController
import os
from view.general_method import CREATICONBUTTON
from view.result_updownload_form import ShowNotiForm
from view.center_windown import center_window 

class FileUploadForm(tk.Toplevel):
    def __init__(self, parent, main_form, remote_directory):
        super().__init__(parent)
        self.root = parent
        self.main_form = main_form
        self.title("Chọn tệp để tải lên")
        self.remote_directory = remote_directory
        self.selected_file_path = None
        
        self.noti_label = tk.Label(self)
        self.noti_label.pack(pady=(20,0))
        
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)
        
        sub_frame1 = ttk.Frame(main_frame)
        sub_frame1.pack(side=tk.TOP, expand=True, padx=10, pady=5)
        self.selectfile_icon, self.selectfile_label = CREATICONBUTTON(self, sub_frame1, "selectfile.png", "Chọn tệp", 8, self.select_file)
        self.file_label = tk.Label(sub_frame1, text="Chưa chọn tệp nào!")
        self.file_label.pack(side=tk.LEFT, pady=10)
        
        sub_frame2 = ttk.Frame(main_frame)
        sub_frame2.pack(side=tk.BOTTOM, padx=30, pady=5)
        ttk.Label(sub_frame2, text="").pack(side=tk.LEFT, expand=True)
        self.exit_icon, self.exit_label = CREATICONBUTTON(self, sub_frame2, "quit.png", "Thoát", 12, self.destroy)
        self.download_icon, self.tftp_label = CREATICONBUTTON(self, sub_frame2, "confirm.png", "Xác nhận", 12, self.upload_file)
        ttk.Label(sub_frame2, text="").pack(side=tk.LEFT, expand=True)
        

    def select_file(self):
        # Mở hộp thoại chọn tệp và lấy đường dẫn của tệp đã chọn
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file_path = file_path
            self.file_label.config(text=f"Đã chọn tệp: {os.path.basename(file_path)}")

    def upload_file(self):
        if self.selected_file_path:
            upload, list_files_in_directory, output = FTPController().upload_FTP(self.remote_directory,self.selected_file_path)
            if upload:
                self.destroy()
                self.main_form.build_folder_tree(list_files_in_directory, "", "/", True)  
            else:
                self.noti_label.config(text=output, fg='red')
        else:
            self.noti_label.config(text="Bạn chưa chọn file!", fg='red')