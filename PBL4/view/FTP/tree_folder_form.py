import sys
sys.path.append("/Users/haison/Downloads/ky7/TestFTP/PBL4")

import tkinter as tk
from tkinter import ttk, PhotoImage
from view.center_windown import center_window 
from view.FTP.uploadFTP_form import FileUploadForm
from view.FTP.downloadFTP_form import FileDownloadForm
from view.FTP.creat_fordel_form import CreatFolderForm
from view.FTP.rename_form import RenameForm
from view.FTP.delete_form import DeleteForm
from PIL import Image, ImageTk
from model.global_resources import filenamelist
from model.global_resources import directoryIMG
from controller.FTP_controller import FTPController

class TreeFolderForm(tk.Toplevel):    
    def build_folder_tree(self, list_files, parent, directory, reload):
        # Xóa tất cả các mục hiện có trong cây thư mục
        if reload:
            for item in self.tree.get_children():
                self.tree.delete(item)
        
        for index, item in enumerate(list_files):
            if item["directory"] == directory:
                if item["type"] == "folder":
                    new_dir = directory + "/" + item["name"]
                    new_parent = self.tree.insert(parent, "end", text=item["name"], open=True, image=self.folder_icon)
                    sub_list_files = list_files[index+1:]
                    self.build_folder_tree(sub_list_files, new_parent, new_dir, False)
                elif item["type"] == "file":
                    self.tree.insert(parent, "end", text=item["name"], image=self.icon_list.get(item["name"].split(".")[-1].lower(), self.default_icon))
                    
    def __init__(self, root, list_files_in_directory):
        super().__init__(root)
        self.root = root
        self.list_files_in_directory = list_files_in_directory
        self.title('Cây thư mục')
        self.configure(background='#323232')
        self.icon_list = {}
        
        # Tạo một frame chứa cây thư mục
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        style = ttk.Style(self)
        style.configure("Treeview", background="#343541", foreground="#FFFFFF", rowheight=30, fieldbackground="#343541")
        style.map("Treeview", background=[('selected', '#309FA6')])
        
        # Tạo cây thư mục
        self.tree = ttk.Treeview(frame, selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        self.default_icon = ImageTk.PhotoImage(Image.open(directoryIMG + "file.png").resize((25, 25), Image.LANCZOS))
        self.folder_icon = ImageTk.PhotoImage(Image.open(directoryIMG + "folder.png").resize((25, 25), Image.LANCZOS))
        for filename in filenamelist:
            self.icon_list.update({filename: ImageTk.PhotoImage(Image.open(directoryIMG+filename+".png").resize((20, 20), Image.LANCZOS))})
        self.build_folder_tree(self.list_files_in_directory, "", "/", True)
        
        style.configure('Custom.TFrame', background='#313232')
        # Tạo một frame chung để chứa tất cả các frames con
        main_frame = ttk.Frame(self, style='Custom.TFrame')
        main_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0,15))
        # Tạo label trống bên trái
        ttk.Label(main_frame, text="").pack(side=tk.LEFT, expand=True)
        
        self.upload_label = ttk.Label()
        self.download_label = ttk.Label()
        self.new_folder_label = ttk.Label()
        
        self.upload_icon_label = ttk.Label()
        self.download_icon_label = ttk.Label()
        self.new_folder_icon_label = ttk.Label()
        
        # Định nghĩa thông tin về các nút và icon tương ứng
        icons_info = [
            ("newfolder.png", "New Folder", self.show_create_new_folder_form),
            ("upload.png", "Upload", self.show_upload_file_form),
            ("download.png", "Download", self.show_download_file_form),
            ("rename.png", "Rename", self.show_rename_form),
            ("delete.png", "Delete", self.show_delete_form),
            ("logout.png", "Logout", self.logout)
        ]
        # Tạo các frames và icon dựa trên thông tin đã định nghĩa
        for icon_filename, button_text, command in icons_info:
            sub_frame = ttk.Frame(main_frame, style='Custom.TFrame')
            sub_frame.pack(side=tk.LEFT, padx=(20))
            # Tải biểu tượng và label đặt vào trong Frame biểu tượng
            icon = PhotoImage(file=directoryIMG + icon_filename).subsample(12, 12)
            icon_label = tk.Label(sub_frame, image=icon)
            icon_label.bind("<Button-1>", lambda event, cmd=command: cmd())  # Sử dụng lambda để gắn hàm đúng
            icon_label.pack(side=tk.TOP)
            label = ttk.Label(sub_frame, text=button_text)
            label.bind("<Button-1>", lambda event, cmd=command: cmd())
            label.pack(side=tk.TOP)
            setattr(self, button_text.replace(" ", "_").lower() + "icon", icon)
            setattr(self, button_text.replace(" ", "_").lower() + "_icon_label", icon_label)
            setattr(self, button_text.replace(" ", "_").lower() + "_label", label)
            
        # Tạo label trống bên phải
        ttk.Label(main_frame, text="").pack(side=tk.LEFT, expand=True)

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            # Lấy tên của mục được chọn
            item_text = self.tree.item(item, "text")
            # Kiểm tra tên mục có phải là đuôi của một tệp hay không (ví dụ: .jpg, .txt)
            # (Điều này giả định rằng tên tệp có đuôi và tên thư mục không có)
            if "." in item_text:
                self.upload_icon_label.unbind("<Button-1>")
                self.new_folder_icon_label.unbind("<Button-1>")
                self.download_icon_label.bind("<Button-1>", lambda event, cmd=self.show_download_file_form: cmd())
                
                self.upload_label.unbind("<Button-1>")
                self.new_folder_label.unbind("<Button-1>")
                self.download_label.bind("<Button-1>", lambda event, cmd=self.show_download_file_form: cmd())
                
                self.upload_label.config(state=tk.DISABLED)
                self.new_folder_label.config(state=tk.DISABLED)
                self.download_label.config(state=tk.NORMAL)
            else:
                self.upload_icon_label.bind("<Button-1>", lambda event, cmd=self.show_upload_file_form: cmd())
                self.new_folder_icon_label.bind("<Button-1>", lambda event, cmd=self.show_create_new_folder_form: cmd())
                self.download_icon_label.unbind("<Button-1>")
                
                self.upload_label.bind("<Button-1>", lambda event, cmd=self.show_upload_file_form: cmd())
                self.new_folder_label.bind("<Button-1>", lambda event, cmd=self.show_create_new_folder_form: cmd())
                self.download_label.unbind("<Button-1>")
                
                self.upload_label.config(state=tk.NORMAL)
                self.new_folder_label.config(state=tk.NORMAL)
                self.download_label.config(state=tk.DISABLED)
                
    def get_full_path(self, item):
        # Khởi tạo danh sách để lưu trữ đường dẫn
        path = []
        # Lấy tên của mục được chọn
        item_text = self.tree.item(item, "text")
        path.insert(0, item_text)  # Thêm tên mục vào danh sách đầu tiên
        # Lặp qua các mục cha cho đến khi gặp thư mục gốc
        parent_item = self.tree.parent(item)
        while parent_item:
            parent_text = self.tree.item(parent_item, "text")
            path.insert(0, parent_text)  # Thêm tên mục cha vào đầu danh sách
            parent_item = self.tree.parent(parent_item)
        # Kết hợp các tên để tạo đường dẫn hoàn chỉnh
        full_path = "/".join(path)
        return full_path
        
    def show_form(self, form_class, width, height):
        selected_items = self.tree.selection()
        if selected_items:
            full_path = self.get_full_path(selected_items[0])
            form = form_class(self, self, "/" + full_path)
            center_window(form, width, height)
            form.mainloop()

    def show_create_new_folder_form(self):
        self.show_form(CreatFolderForm, 400, 340)
        
    def show_upload_file_form(self):
        self.show_form(FileUploadForm, 400, 300)

    def show_download_file_form(self):
        self.show_form(FileDownloadForm, 500, 320)

    def show_rename_form(self):
        self.show_form(RenameForm, 400, 270)
    
    def show_delete_form(self):
        self.show_form(DeleteForm, 400, 220)

    def logout(self):
        FTPController().logout_ftp()
        self.root.deiconify()  # Hiển thị lại cửa sổ chính
        self.destroy()  # Hủy cửa sổ TreeFolderForm hiện tại
