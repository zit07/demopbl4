import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import PhotoImage, ttk
from model.global_resources import directoryIMG
import re

def CREATICONBUTTON(self, frame, image_name, text, size, command):
    sub_frame = ttk.Frame(frame)
    sub_frame.pack(side=tk.LEFT, padx=30)
    icon = PhotoImage(file=directoryIMG + image_name).subsample(size, size)
    icon_label = tk.Label(sub_frame, image=icon)
    icon_label.bind("<Button-1>", lambda event, cmd=command: cmd())
    icon_label.pack(side=tk.TOP, pady=10)
    label = ttk.Label(sub_frame, text=text)
    label.bind("<Button-1>", lambda event, cmd=command: cmd())
    label.pack(side=tk.TOP)
    return icon, label

def is_strong_password(new_password):
    
    # Kiểm tra có ít nhất một ký tự viết hoa
    # if not re.search(r'[A-Z]', new_password):
    #     return False

    # Kiểm tra có ít nhất một ký tự viết thường
    if not re.search(r'[a-z]', new_password):
        return False, "Thiếu một ký từ viết thường"

    # Kiểm tra có ít nhất một chữ số
    if not re.search(r'[0-9]', new_password):
        return False, "Thiếu một chữ số"

    # Kiểm tra có ít nhất một ký tự đặc biệt
    # if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\]', new_password):
    #     return False
    
    # Kiểm tra mật khẩu không quá trùng lặp
    if re.search(r'(.)\1{2,}', new_password):
        return False, "Mật khẩu quá trùng lặp ký tự"
    
    # Kiểm tra mật khẩu không quá đơn giản hoặc dễ đoán
    common_passwords = ['123456', 'password', 'admin']
    if new_password in common_passwords:
        return False, "Mật khẩu đơn giản dễ đoán"

    return True, ""