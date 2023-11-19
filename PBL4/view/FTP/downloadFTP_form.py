import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import filedialog, ttk
from controller.FTP_controller import FTPController
import os
from view.result_updownload_form import ShowNotiForm
from view.center_windown import center_window 
from view.general_method import CREATICONBUTTON

class FileDownloadForm(tk.Toplevel): 
    def __init__(self, parent, main_form, remote_file_path):
        super().__init__(parent)
        self.root = parent
        self.main_form = main_form
        self.remote_file_path = remote_file_path  # Đường dẫn của tệp cần tải về
        self.local_directory_path = None  # Đường dẫn của thư mục để lưu tệp
        self.title("Tải xuống tệp tin bằng FTP")

        self.noti_label = tk.Label(self)
        self.noti_label.pack(pady=(20,0))
        
        form_frame = ttk.Frame(self)
        form_frame.pack(fill=tk.BOTH, pady=(20,0), expand=True)
        
        sub_frame1 = ttk.Frame(form_frame)
        sub_frame1.pack(side=tk.TOP, padx=(20))
        self.filename_label = tk.Label(sub_frame1, text="Lưu với tên:")
        self.filename_label.pack(side=tk.LEFT, pady=10)
        self.file_name_entry = tk.Entry(sub_frame1, width=30)
        self.file_name_entry.pack(side=tk.LEFT, pady=10)
        self.file_name_entry.insert(0, remote_file_path.split("/")[-1])
        
        sub_frame2 = ttk.Frame(form_frame)
        sub_frame2.pack(side=tk.TOP, padx=(20))
        self.selectfolder_icon, self.selectfolder_label = CREATICONBUTTON(self, sub_frame2, "selectfolder.png", "Chọn thư mục", 12, self.select_directory)
        self.selected_directory_label = tk.Label(sub_frame2, text="Chưa chọn thư mục nào!", width=30)
        self.selected_directory_label.pack(side=tk.LEFT, pady=10, padx=40)
        
        sub_frame3 = ttk.Frame(form_frame)
        sub_frame3.pack(side=tk.TOP, pady=(20))
        ttk.Label(sub_frame3, text="").pack(side=tk.LEFT, expand=True)
        self.quit_icon, self.quit_label = CREATICONBUTTON(self, sub_frame3, "quit.png", "Thoát", 12, self.destroy)
        self.confirm_icon, self.confirm_label = CREATICONBUTTON(self, sub_frame3, "confirm.png", "Xác nhận", 12, self.download_file)
        ttk.Label(sub_frame3, text="").pack(side=tk.LEFT, expand=True)
        

    def select_directory(self):
        # Mở hộp thoại chọn thư mục và lấy đường dẫn của thư mục đã chọn
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory_label.config(text=f"Thư mục đã chọn: {os.path.basename(os.path.normpath(directory))}")
            self.local_directory_path = directory  # Lưu đường dẫn đã chọn vào biến

    def download_file(self):
        # Lấy tên tệp từ Entry
        file_name = self.file_name_entry.get()
        if not file_name:
            self.noti_label.config(text="Vui lòng nhập tên cho tệp!", fg='red')
            return
        elif not "." in file_name:
            self.noti_label.config(text="Thiếu kiểu cho tên tệp tin cần tải về (.txt, .pdf...)!", fg='red')
            return
        else:
            if self.local_directory_path:
                # Kết hợp đường dẫn và tên tệp để tạo đường dẫn lưu trữ tệp
                download, output = FTPController().download_FTP(self.remote_file_path, os.path.join(self.local_directory_path, file_name))
                self.download_success() if download else self.noti_label.config(text=output, fg='red')
            else:
                self.noti_label.config(text="Vui lòng chọn thư mục để lưu!", fg='red')
        
    def download_success(self):
        self.destroy()
        formresultdown = ShowNotiForm(self.root, "Tải xuống thành công!",  "successdownload")
        center_window(formresultdown, 450, 280)
        formresultdown.mainloop()
