import tkinter as tk
from model.global_resources import directoryIMG
from tkinter import PhotoImage

class ShowNotiForm(tk.Toplevel):
    def __init__(self, parent, message, iconname):
        super().__init__(parent)
        self.title("Thông báo")
        
        # Load và hiển thị icon
        self.photo = PhotoImage(file=directoryIMG+iconname+".png").subsample(6, 6)
        self.icon_label = tk.Label(self, image=self.photo)
        self.icon_label.pack(side="top", pady=20)
        
        # Thêm message
        message_label = tk.Label(self, text=message)
        message_label.pack(side="top", pady=10)
        
        # Thêm nút OK
        ok_button = tk.Button(self, text="OK", command=self.destroy)
        ok_button.pack(side="top", pady=10)
        
        # Thiết lập kích thước và vị trí cửa sổ
        self.geometry("+{}+{}".format(parent.winfo_x()+50, parent.winfo_y()+50))
        self.grab_set()  # Đảm bảo không có widget nào khác có thể tương tác khi hộp thoại này đang mở


