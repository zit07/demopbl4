import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import scrolledtext, ttk, font as tkFont
from model.global_resources import host, UsernameSSH
from controller.SSH_controller import SSHController
from view.center_windown import center_window
from view.general_method import CREATICONBUTTON
from view.SSH.add_user_form import AddUserForm
from view.SSH.delete_user_form import DeleteUser
from view.SSH.change_password_form import ChangePassword
from view.SSH.reset_password_form import ResetPassword


class MainFormSSH(tk.Toplevel):
    def __init__(self, root, checkroot):
        super().__init__(root)
        self.root = root
        self.checkroot = checkroot
        self.title('SSH Terminal')
        
        font = tkFont.Font(family="Monospace", size=13)
        self.terminal_text = scrolledtext.ScrolledText(self, font=font, wrap='word', bg='#1F1F1F', fg='white')
        self.terminal_text.pack(fill=tk.BOTH, expand=1)
        
        # Tạo tag mới với cấu hình màu mong muốn
        self.terminal_text.tag_config('prompt', foreground='green')
        
        # Xử lý sự kiện khi nhấn phím Enter
        self.terminal_text.bind("<Return>", self.execute_command)
        self.terminal_text.bind("<KeyPress>", lambda e: 'break' if e.keysym == 'Up' or e.keysym == 'Down' else None)
        self.insert_prompt()

        main_frame = ttk.Frame(self, style='Custom.TFrame')
        main_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0,5))
        ttk.Label(main_frame, text="").pack(side=tk.LEFT, expand=True)
        if self.checkroot:
            self.adduser_icon, self.adduser_label = CREATICONBUTTON(self, main_frame, 'adduser.png', 'Thêm người dùng', 8, self.show_form_adduser)
            self.deleteuser_icon, self.deleteuser_label = CREATICONBUTTON(self, main_frame, 'deleteuser.png', 'Xoá người dùng', 8, self.show_form_deleteuser)
            self.resetpassword_icon, self.resetpassword_label = CREATICONBUTTON(self, main_frame, 'resetpassword.png', 'Reset mật khẩu', 8, self.show_form_resetpass)
        self.changepass_icon, self.changepass_label = CREATICONBUTTON(self, main_frame, 'changepass.png', 'Đổi mật khẩu', 8, self.show_form_changepass)
        self.logout_icon, self.logout_label = CREATICONBUTTON(self, main_frame, 'logout.png', 'Đăng xuất', 8, self.backhome)
        ttk.Label(main_frame, text="").pack(side=tk.LEFT, expand=True)
        
        
        # Đặt focus vào ScrolledText widget
        self.terminal_text.focus_set()
        
    def execute_command(self, event, output=""):
        if output == "":
            command = self.terminal_text.get("prompt_end", "insert lineend").strip()
            if command == "clear":
                self.terminal_text.delete('1.0', tk.END)
            elif command == "quit":
                self.backhome()
            elif self.checkroot and "deluser" in command:
                self.show_form_deleteuser()
            elif self.checkroot and "adduser" in command:
                self.show_form_deleteuser()
            elif command != "":
                # Thực hiện câu lệnh
                output = SSHController().execute_ssh(command)
        
        self.terminal_text.insert(tk.END, f'\n{output}')
        if output !="":
            self.terminal_text.insert(tk.END, f'\n')
        self.insert_prompt()

        # Ngăn không cho sự kiện 'Return' tiếp tục để tránh tạo dòng mới thừa
        return 'break'

    def insert_prompt(self):
        self.terminal_text.insert(tk.END, f'{UsernameSSH().get_username()}@{host}:~$ ', 'prompt')
        self.terminal_text.mark_set("prompt_end", tk.END)
        self.terminal_text.see(tk.END)
        self.terminal_text.insert(tk.INSERT, "")
        self.terminal_text.mark_set("prompt_end", "insert")
        # Di chuyển con trỏ về sau dấu nhắc mới
        self.terminal_text.mark_gravity("prompt_end", tk.LEFT)
    
    def backhome(self):
        SSHController().logout_ssh()
        self.root.deiconify()  # Hiển thị lại cửa sổ chính
        self.destroy()  # Hủy cửa sổ hiện tại
    
    def show_form(self, form_class, width, height):
        form = form_class(self.root, self)
        center_window(form, width, height)
        form.mainloop()
        
    def show_form_adduser(self):
        self.show_form(AddUserForm, 400, 330)
        
    def show_form_deleteuser(self):
        self.show_form(DeleteUser, 400, 330)
        
    def show_form_changepass(self):
        self.show_form(ChangePassword, 400, 330)
        
    def show_form_resetpass(self):
        self.show_form(ResetPassword, 400, 330)