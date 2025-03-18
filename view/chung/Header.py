import tkinter as tk


class Header:
    def __init__(self, root, title):
        self.root = root
        self.header_frame = tk.Frame(root, bg="white", height=50)
        self.header_frame.pack(fill=tk.X)

        # Logo
        logo_frame = tk.Frame(self.header_frame, bg="white")
        logo_frame.pack(side=tk.LEFT, padx=20)

        logo_label = tk.Label(logo_frame, text=title, font=("Arial", 18, "bold"),
                              fg="#1a3f66", bg="white")
        logo_label.pack(side=tk.LEFT)

        # User info on right
        user_frame = tk.Frame(self.header_frame, bg="white")
        user_frame.pack(side=tk.RIGHT, padx=20)

        # User icon
        self.user_icon = tk.Label(user_frame, text="👤", bg="white", font=("Arial", 14), cursor="hand2")
        self.user_icon.pack(side=tk.LEFT, padx=5)

        # Gán sự kiện click
        self.user_icon.bind("<Button-1>", self.on_user_icon_click)

    def on_user_icon_click(self, event):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view.chung.ThongTin import ThongTin
        ThongTin(self.root)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = Header(root)
#     root.mainloop()