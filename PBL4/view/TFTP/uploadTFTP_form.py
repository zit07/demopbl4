import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import filedialog
from controller.TFTP_controller import TFTPController
from view.result_updownload_form import ShowNotiForm
from view.center_windown import center_window 
from view.general_method import CREATICONBUTTON
from tkinter import ttk
import os

class FileUploadForm(tk.Toplevel):
    def __init__(self, parent, main_form):
        super().__init__(parent)
        self.root = parent
        self.main_form = main_form
        self.title("Tải lên tệp tin bằng TFTP")
        self.selected_file_path = None

        # Tạo label hiển thị đường dẫn tệp đã chọn
        self.noti_label = tk.Label(self, text="")
        self.noti_label.pack(pady=(20,0))

        # Tạo một frame chứa tiêu đề và Entry
        form_frame = ttk.Frame(self)
        form_frame.pack(fill=tk.BOTH, pady=(20,0), expand=True)

        #chon file
        sub_frame2 = ttk.Frame(form_frame)
        sub_frame2.pack(side=tk.TOP, padx=(20))
        self.selectfile_icon, self.selectfile_label = CREATICONBUTTON(self, sub_frame2, "selectfile.png", "Chọn tệp", 12, self.select_file)
        self.selected_file_label = tk.Label(sub_frame2, text="Chưa chọn tệp tin nào!", width=30)
        self.selected_file_label.pack(side=tk.LEFT, pady=10, padx=40)
        
        # Tiêu đề "Nhập tên file"
        sub_frame1 = ttk.Frame(form_frame)
        sub_frame1.pack(side=tk.TOP, padx=(20))
        self.filename_label = tk.Label(sub_frame1, text="Đặt tên cho file:")
        self.filename_label.pack(side=tk.LEFT, pady=10)
        self.file_name_entry = tk.Entry(sub_frame1, width=40)
        self.file_name_entry.pack(side=tk.LEFT, pady=10)
        self.file_name_entry.insert(0, "")  
        
        sub_frame3 = ttk.Frame(form_frame)
        sub_frame3.pack(side=tk.BOTTOM, pady=(20))
        ttk.Label(sub_frame3, text="").pack(side=tk.LEFT, expand=True)
        self.quit_icon, self.quit_label = CREATICONBUTTON(self, sub_frame3, "quit.png", "Thoát", 12, self.destroy)
        self.confirm_icon, self.confirm_label = CREATICONBUTTON(self, sub_frame3, "confirm.png", "Xác nhận", 12, self.upload_file)
        ttk.Label(sub_frame3, text="").pack(side=tk.LEFT, expand=True)

        
    def select_file(self):
        # Mở hộp thoại chọn tệp và lấy đường dẫn của tệp đã chọn
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file_path = file_path
            self.selected_file_label.config(text=f"Đã chọn tệp: {os.path.basename(self.selected_file_path)}")
            # Gắn tên tệp vào entry
            self.file_name_entry.delete(0, tk.END)  # Xóa nội dung hiện có
            self.file_name_entry.insert(0, self.selected_file_path.split("/")[-1])

    def upload_file(self):
        if self.selected_file_path:
            filename = self.file_name_entry.get()
            if not filename:
                self.noti_label.config(text="Đặt tên cho tệp tin trên máy chủ!", fg='red')
                return
            elif not "." in filename:
                self.noti_label.config(text="Tên thiếu kiểu tệp tin (.txt, .pdf...)!", fg='red')
                return
            upload = TFTPController().upload_TFTP(self.selected_file_path, filename)
            self.show_result(upload)
            
        else:
            self.noti_label.config(text="Bạn chưa chọn tệp tin để tải lên!", fg='red')
            
            
    def show_result(self, success):
        message, tag = ("Tải lên thành công!", "successupload") if success else ("Tải lên thất bại!", "errorupload")
        formresultdown = ShowNotiForm(self.root if success else self, message, tag)
        center_window(formresultdown, 450, 280)
        if success:
            self.destroy()
        formresultdown.mainloop()
        