import tkinter as tk
from tkinter import messagebox

# Hàm này sẽ được gọi khi nút được bấm
def button_click():
    messagebox.showinfo("Thông báo", "Nút đã được bấm!")

# Tạo cửa sổ giao diện
window = tk.Tk()
window.title("Chương trình Python với giao diện")

# Tạo một nút và đặt hàm gọi khi nút được bấm
button = tk.Button(window, text="Bấm vào tôi!", command=button_click)
button.pack()

# Bắt đầu vòng lặp chính
window.mainloop()
