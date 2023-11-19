import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk
from view.center_windown import center_window
from view.TFTP.downloadTFTP_form import FileDownloadForm
from view.TFTP.uploadTFTP_form import FileUploadForm
from view.general_method import CREATICONBUTTON

class MainFormTFTP(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.title('Ứng dụng Upload/Download TFTP')

        # Tạo một frame để chứa nút lựa chọn và đặt nó ở giữa cửa sổ
        frame = ttk.Frame(self)
        frame.pack(pady=(self.winfo_screenheight()//4)) # Đặt padding để frame nằm ở giữa cửa sổ theo chiều dọc

        self.back_icon, self.back_label = CREATICONBUTTON(self, frame,'back.png', 'Quay lại', 6, self.back)
        self.uploadload_icon, self.uploadload_label = CREATICONBUTTON(self, frame,'upload.png', 'Upload', 6, self.show_upload_TFTP_form)
        self.download_icon, self.download_label = CREATICONBUTTON(self, frame,'download.png', 'Download', 6, self.show_download_TFTP_form)
        
    def show_form(self, form_class, width, height):
        form = form_class(self.root, self)
        center_window(form, width, height)
        form.mainloop()

    def show_upload_TFTP_form(self):
        self.show_form(FileUploadForm, 550, 320)

    def show_download_TFTP_form(self):
        self.show_form(FileDownloadForm, 550, 320)
        
    def back(self):
        self.root.deiconify()
        self.destroy()