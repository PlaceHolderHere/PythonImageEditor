import image_functions
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk

# Constants
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
PHOTO_WIDTH: int = SCREEN_WIDTH - 320
PHOTO_HEIGHT: int = SCREEN_HEIGHT - 180
PRIMARY_COLOR:str = "#C3D5EF"
ACCENT_COLOR:str = "#26384D"
SIDEBAR_WIDTH: int = 88
NAVBAR_HEIGHT: int = 64
PLACEHOLDER_PHOTO: str = "assets/placeholder-photo.png"
VALID_FILE_EXTENSIONS: dict[str, int] = {".png": 0, ".pgm": 0, ".ppm": 0, ".gif": 0}

# Formatting a string for filedialog option
# UPLOAD_BUTTON_EXTENSIONS: str = "*.png *.pgm *.ppm *.gif"
UPLOAD_BUTTON_EXTENSIONS: str = "*.*"

# NOTE:
# Currently PhotoImage in tkinter only supports 4 file types, however PIL supports a lot more
# In the future I'll convert the inputted image into a png for display purposes and store it in ./assets

# Classes
class PythonImageEditor:
    def __init__(self):
        # Tkinter Initialization
        self.root = tk.Tk()
        self.root.title("Python Image Editor")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)

        # NavBar
        self.navbar_frame = tk.Frame(self.root, bg=ACCENT_COLOR, width=SCREEN_WIDTH, height=NAVBAR_HEIGHT)
        self.navbar_frame.pack(side="top", padx=0, pady=0, fill="x")

        self.upload_button = tk.Button(self.navbar_frame, text="upload", command=self.upload_function)
        self.upload_button.pack(side="left", padx=16, pady=20)

        # SideBar
        self.sidebar_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, width=SIDEBAR_WIDTH, height=SCREEN_HEIGHT)
        self.sidebar_frame.pack(side="left")

        # Content Area
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Photo
        self.photo_canvas = tk.Canvas(self.content_frame, width=PHOTO_WIDTH, height=PHOTO_HEIGHT, highlightthickness=0)
        self.photo_canvas.pack(expand=True)

        self.photo_path = PLACEHOLDER_PHOTO
        self.pillow_photo = Image.open(self.photo_path)
        self.resized_photo = ImageOps.contain(self.pillow_photo, (PHOTO_WIDTH, PHOTO_HEIGHT))
        self.display_photo = ImageTk.PhotoImage(self.resized_photo)
        self.photo_id = self.photo_canvas.create_image(PHOTO_WIDTH // 2, PHOTO_HEIGHT // 2,
                                                       image=self.display_photo, anchor="center")

        # Main Loop
        self.root.mainloop()

    def upload_function(self) -> None:
        selected_path = filedialog.askopenfilename(
            title="Select a Photo to Edit",
            filetypes=[("Photos", UPLOAD_BUTTON_EXTENSIONS)],
        )

        # Checking if a file was selected
        if selected_path:
            if self.verify_image_path(selected_path):
                # Updating Related Variables/Labels After Selecting a new Photo
                self.pillow_photo.close()
                self.photo_path = selected_path
                self.pillow_photo = Image.open(self.photo_path)
                self.resized_photo = ImageOps.contain(self.pillow_photo, (PHOTO_WIDTH, PHOTO_HEIGHT))
                self.display_photo = ImageTk.PhotoImage(self.resized_photo)
                self.photo_canvas.itemconfig(self.photo_id, image=self.display_photo)
            else:
                self.create_error_popup("Invalid Input Image! Please try uploading again.", (400, 100))


    @staticmethod
    def verify_image_path(path: str) -> bool:
        if not os.path.exists(path):
            return False

        name, ext = os.path.splitext(path)
        if ext.lower() not in VALID_FILE_EXTENSIONS:
            return False
        return True

    def create_error_popup(self, message: str, size: tuple[int, int]) -> None:
        # Creating a pop-up to show an error
        popup = tk.Toplevel(self.root)
        popup.title("Error!")
        popup.geometry(f"{size[0]}x{size[1]}")
        popup.resizable(False, False)
        popup.grab_set()  # blocks user from performing other actions unless pop-up is closed
        self.root.eval(f"tk::PlaceWindow {popup} center")  # centers popup

        # Error Message
        label = tk.Label(popup, text=message, font=("Arial", 12), pady=20)
        label.pack()

        close_btn = tk.Button(popup, text="Close", width=7, height=2, command=popup.destroy, bg=PRIMARY_COLOR)
        close_btn.pack()

if __name__ == "__main__":
    PythonImageEditor()