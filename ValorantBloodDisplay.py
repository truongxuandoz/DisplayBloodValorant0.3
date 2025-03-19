import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
import sys
from typing import List
from pathlib import Path
import logging
import traceback
import tempfile
import atexit

def get_base_path():
    """Get the base path for the application, works both for exe and script."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(sys.argv[0]).parent

def extract_resources():
    """Extract embedded resources to a temporary directory."""
    temp_dir = Path(tempfile.mkdtemp())
    base_path = get_base_path()
    
    # Copy embedded files to temp directory
    for filename in ["MatureData-WindowsClient.pak", "MatureData-WindowsClient.sig"]:
        src = base_path / filename
        if src.exists():
            shutil.copy2(src, temp_dir / filename)
    
    # Register cleanup on exit
    atexit.register(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
    return temp_dir

# Extract resources at startup
TEMP_RESOURCE_DIR = extract_resources()

class ModernUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Valorant Blood Display")
        self.geometry("700x600")
        self.minsize(600, 500)
        
        # Configure the grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Set theme and colors
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Define colors
        self.accent_color = "#ff4444"
        self.hover_color = "#cc3333"
        self.bg_color = "#1a1a1a"
        self.secondary_color = "#2d2d2d"
        
        # Define fonts that support Vietnamese
        self.font_family = "Segoe UI"  # Excellent Vietnamese support and modern look
        
        self.configure(fg_color=self.bg_color)
        
        self.manager = ValorantManager(self)
        self.create_widgets()
        
    def show_tutorial(self):
        """Display tutorial window with instructions."""
        tutorial = ctk.CTkToplevel(self)
        tutorial.title("Tutorial")
        tutorial.geometry("600x400")
        tutorial.resizable(False, False)
        tutorial.grab_set()  # Make it modal
        
        # Set icon if available
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                
            icon_path = os.path.join(application_path, "valorant_icon.ico")
            if os.path.exists(icon_path):
                tutorial.iconbitmap(icon_path)
        except Exception:
            pass  # Ignore icon errors
        
        # Configure the grid layout
        tutorial.grid_columnconfigure(0, weight=1)
        tutorial.grid_rowconfigure(0, weight=1)
        
        # Create frame
        content_frame = ctk.CTkFrame(tutorial, fg_color=self.secondary_color)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="How to Use Valorant Blood Display",
            font=ctk.CTkFont(family=self.font_family, size=20, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=(20, 10))
        
        # Tutorial text
        tutorial_text = ctk.CTkTextbox(
            content_frame,
            font=ctk.CTkFont(family=self.font_family, size=12),
            wrap="word",
            fg_color="transparent",
            text_color="#ffffff"
        )
        tutorial_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        instructions = """1. Chọn Thư Mục Valorant:
• Nhấn nút 'Chọn Thư Mục'
• Điều hướng đến thư mục cài đặt Valorant của bạn
• Chọn thư mục VALORANT tại: C:/Program Files/Riot Games/VALORANT
  (có thể có vị trí thư mục khác nhau, vì vậy hãy tìm phần chính xác)
• Nhấn 'Chọn Thư Mục' để xác nhận

2. Áp Dụng Hiển Thị Máu:
• Sau khi chọn thư mục, nhấn 'Áp Dụng Hiển Thị Máu'
• Chờ quá trình hoàn tất
• Bạn sẽ thấy thông báo thành công khi hoàn thành

3. Lưu Ý Quan Trọng:
• Đảm bảo rằng Trình Duyệt Riot đang chạy trong khi áp dụng thay đổi (không phải Valorant)
• Khi áp dụng xong, hãy khởi động trò chơi
• Bạn có thể cần chạy ứng dụng với tư cách quản trị viên
• Nếu bạn thấy bất kỳ lỗi nào, hãy kiểm tra thông báo trạng thái
• Thay đổi sẽ có hiệu lực khi bạn khởi động lại Valorant

4. Xử Lý Sự Cố:
• Nếu bạn gặp lỗi quyền truy cập, hãy chạy với tư cách quản trị viên
• Đảm bảo rằng bạn đã chọn thư mục Valorant chính xác
• Kiểm tra khu vực trạng thái để xem bất kỳ thông báo lỗi nào
• Liên hệ với Dylan (xuantruong.software@gmail.com | Discord: dylandoz)"""
        
        tutorial_text.insert("1.0", instructions)
        tutorial_text.configure(state="disabled")
        
        # Close button
        close_button = ctk.CTkButton(
            content_frame,
            text="Đóng Hướng Dẫn",
            command=tutorial.destroy,
            font=ctk.CTkFont(family=self.font_family, size=12, weight="bold"),
            fg_color=self.accent_color,
            hover_color=self.hover_color,
            height=35
        )
        close_button.pack(pady=(0, 20))
        
    def create_widgets(self):
        # Create main frame with rounded corners
        main_frame = ctk.CTkFrame(
            self,
            fg_color=self.secondary_color,
            corner_radius=15
        )
        main_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)  # Make the bottom row expandable
        
        # Credit label at the very top
        credit_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.accent_color,
            corner_radius=8,
            height=40
        )
        credit_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        credit_frame.grid_columnconfigure(0, weight=1)
        credit_frame.grid_propagate(False)
        
        credit_label = ctk.CTkLabel(
            credit_frame,
            text="Made by Dylan",
            font=ctk.CTkFont(family=self.font_family, size=20, weight="bold"),
            text_color="#ffffff"
        )
        credit_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title frame with tutorial button
        title_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        title_frame.grid(row=1, column=0, padx=20, pady=(30, 0), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)  # Center title
        
        # Title in center
        title = ctk.CTkLabel(
            title_frame, 
            text="VALORANT HIỂN THỊ MÁU",
            font=ctk.CTkFont(family=self.font_family, size=32, weight="bold"),
            text_color="#ffffff"
        )
        title.grid(row=0, column=0)
        
        # Subtitle with accent color
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Bật hiệu ứng máu trong trò chơi của bạn",
            font=ctk.CTkFont(family=self.font_family, size=14),
            text_color=self.accent_color
        )
        subtitle.grid(row=2, column=0, pady=(10, 20))
        
        # Separator
        separator = ctk.CTkFrame(
            main_frame,
            height=2,
            fg_color=self.accent_color
        )
        separator.grid(row=2, column=0, padx=40, pady=(0, 30), sticky="ew")
        
        # Valorant folder frame with subtle background
        folder_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.bg_color,
            corner_radius=10
        )
        folder_frame.grid(row=3, column=0, padx=30, pady=(0, 20), sticky="ew")
        folder_frame.grid_columnconfigure(0, weight=1)
        
        self.folder_label = ctk.CTkLabel(
            folder_frame,
            text="THƯ MỤC CÀI ĐẶT ĐƯỜNG DẪN XXX/RIOTGAMES/VALORANT",
            font=ctk.CTkFont(family=self.font_family, size=12, weight="bold"),
            text_color="#ffffff"
        )
        self.folder_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")
        
        self.folder_path = ctk.CTkLabel(
            folder_frame,
            text="Chưa chọn",
            font=ctk.CTkFont(family=self.font_family, size=12),
            text_color="#888888"
        )
        self.folder_path.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")
        
        # Button frame
        button_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        button_frame.grid(row=4, column=0, pady=(10, 20), sticky="nsew")
        
        # Center frame for buttons
        center_button_frame = ctk.CTkFrame(
            button_frame,
            fg_color="transparent"
        )
        center_button_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Select folder button with hover effect
        self.select_button = ctk.CTkButton(
            center_button_frame,
            text="Chọn Thư Mục",
            command=self.select_folder,
            font=ctk.CTkFont(family=self.font_family, size=15, weight="bold"),
            width=160,
            height=45,
            corner_radius=10,
            fg_color="#3498db",  # Bright blue
            hover_color="#2980b9",  # Darker blue
            border_width=2,
            border_color="#2980b9"
        )
        self.select_button.grid(row=0, column=0, padx=15)
        
        # Tutorial button with hover effect
        self.tutorial_button = ctk.CTkButton(
            center_button_frame,
            text="Hướng Dẫn",
            command=self.show_tutorial,
            font=ctk.CTkFont(family=self.font_family, size=15, weight="bold"),
            width=130,
            height=45,
            corner_radius=10,
            fg_color="#2ecc71",  # Bright green
            hover_color="#27ae60",  # Darker green
            border_width=2,
            border_color="#27ae60"
        )
        self.tutorial_button.grid(row=0, column=1, padx=15)
        
        # Apply button with hover effect
        self.apply_button = ctk.CTkButton(
            center_button_frame,
            text="Áp Dụng Hiển Thị Máu",
            command=self.apply_changes,
            font=ctk.CTkFont(family=self.font_family, size=15, weight="bold"),
            width=220,
            height=45,
            corner_radius=10,
            fg_color="#e74c3c",  # Bright red
            hover_color="#c0392b",  # Darker red
            border_width=2,
            border_color="#c0392b"
        )
        self.apply_button.grid(row=0, column=2, padx=15)
        
        # Status frame with custom background
        status_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.bg_color,
            corner_radius=10
        )
        status_frame.grid(row=5, column=0, padx=30, pady=(0, 30), sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Status label
        status_label = ctk.CTkLabel(
            status_frame,
            text="TRẠNG THÁI",
            font=ctk.CTkFont(family=self.font_family, size=16, weight="bold"),
            text_color="#ffffff"
        )
        status_label.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="w")
        
        # Status text with custom styling
        self.status_text = ctk.CTkTextbox(
            status_frame,
            height=100,
            font=ctk.CTkFont(family=self.font_family, size=12),
            wrap="word",
            fg_color=self.bg_color,
            border_width=0,
            text_color="#cccccc"
        )
        self.status_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        self.status_text.insert("1.0", "Sẵn sàng áp dụng hiệu ứng hiển thị máu...\n")
        self.status_text.configure(state="disabled")
        
    def select_folder(self):
        """Handle folder selection button click."""
        folder = filedialog.askdirectory(
            title="Select Valorant Folder",
            initialdir="C:/Program Files/Riot Games/VALORANT"
        )
        if folder:
            self.folder_path.configure(
                text=folder,
                text_color="#ffffff"  # Change color when folder is selected
            )
            self.update_status("✓ Valorant folder selected successfully")
            try:
                self.manager.config_file.write_text(folder)
                logging.info(f"Valorant folder set to: {folder}")
            except Exception as e:
                logging.error(f"Could not save Valorant folder path: {str(e)}")
            
    def apply_changes(self):
        """Handle apply button click."""
        folder = self.folder_path.cget("text")
        if not folder or folder == "Not selected":
            self.update_status("⚠ Please select Valorant folder first")
            messagebox.showwarning("Warning", "Please select Valorant folder first")
            return
        self.update_status("⌛ Applying changes...")
        self.manager.process_files()
            
    def update_status(self, message: str):
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"\n{message}")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")

class ValorantManager:
    """Manages Valorant game files for blood display modification."""
    
    def __init__(self, ui: ModernUI):
        self.ui = ui
        self.config_dir = Path(os.getenv('APPDATA')) / "ValorantBloodDisplay"
        self.config_file = self.config_dir / "valorant_path.txt"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        log_file = self.config_dir / "app.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def process_files(self) -> None:
        """Main process to handle file operations."""
        try:
            valorant_folder = Path(self.ui.folder_path.cget("text"))
            if not valorant_folder.exists():
                raise ValueError("Selected folder does not exist")

            pak_path = valorant_folder / "live/ShooterGame/Content/Paks"
            if not pak_path.exists():
                raise ValueError("Invalid Valorant installation folder")

            # Copy files from temp directory
            for filename in ["MatureData-WindowsClient.pak", "MatureData-WindowsClient.sig"]:
                src = TEMP_RESOURCE_DIR / filename
                dst = pak_path / filename
                if src.exists():
                    shutil.copy2(src, dst)
                    logging.info(f"Copied {filename} to {dst}")

            self.ui.update_status("✓ Blood display effects applied successfully!")
            messagebox.showinfo("Success", "Blood display effects have been applied successfully!")

        except Exception as e:
            error_msg = str(e)
            logging.error(f"Error processing files: {error_msg}\n{traceback.format_exc()}")
            self.ui.update_status(f"⚠ Error: {error_msg}")
            messagebox.showerror("Error", f"Failed to apply blood display effects:\n{error_msg}")

def main():
    """Entry point of the application."""
    try:
        app = ModernUI()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", 
            "The application encountered a critical error and needs to close.\n\n" + str(e))

if __name__ == "__main__":
    main()