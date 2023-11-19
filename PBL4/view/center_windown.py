def center_window(root, width, height):
    # Lấy kích thước màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Tính toán vị trí của cửa sổ
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Đặt vị trí cửa sổ
        root.geometry(f"{width}x{height}+{x}+{y}")
        