import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import BOTTOM, ttk
from controller.FTP_controller import FTPController
from view.general_method import CREATICONBUTTON

class DeleteForm(tk.Toplevel):
    def __init__(self, parent, main_form, remote_path):
        super().__init__(parent)
        self.main_form = main_form
        self.remote_path = remote_path 
        self.title("Xoá")

        self.attention_label = tk.Label(self, text="Tệp hoặc thư mục đã xoá sẽ không thể khôi phục", fg='red')
        self.attention_label.pack(pady=(40,10))

        self.noti_label = tk.Label(self)
        self.noti_label.pack()
        
        # Tạo frame để đặt nút "Xác nhận" và "Thoát" cùng trên một hàng ngang
        form_frame = tk.Frame(self)
        form_frame.pack(side=BOTTOM, pady=20)

        sub_frame1 = ttk.Frame(form_frame)
        sub_frame1.pack(side=tk.TOP, padx=(20))
        self.quit_icon, self.quit_label = CREATICONBUTTON(self, sub_frame1, "quit.png", "Thoát", 12, self.destroy)
        self.confirm_icon, self.confirm_label = CREATICONBUTTON(self, sub_frame1, "confirm.png", "Xác nhận xoá", 12, self.delete)


    def delete(self):
        if self.remote_path:
            delete, err, list_files_in_directory = FTPController().delete(self.remote_path)
            if delete:
                self.destroy()
                self.main_form.build_folder_tree(list_files_in_directory, "", "/", True)  
            else:
                self.noti_label.config(text=err, fg='red')
