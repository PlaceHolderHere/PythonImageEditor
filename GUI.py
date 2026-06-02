import image_functions
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PHOTO_WIDTH = SCREEN_WIDTH - 320
PHOTO_HEIGHT = SCREEN_HEIGHT - 180
PRIMARY_COLOR = "#C3D5EF"
ACCENT_COLOR = "#26384D"
SIDEBAR_WIDTH = 88
NAVBAR_HEIGHT = 64
PLACEHOLDER_PHOTO = "assets/placeholder-photo.png"
VALID_FILE_EXTENSIONS = {".png": 0, ".pgm": 0, ".ppm": 0, ".gif": 0}

# Formatting a string for filedialog option
UPLOAD_BUTTON_EXTENSIONS = "*.png *.pgm *.ppm *.gif"

# NOTE:
# Currently PhotoImage in tkinter only supports 4 file types, however PIL supports a lot more
# In the future I'll convert the inputted image into a png for display purposes and store it in ./assets

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
        self.photo_canvas = tk.Canvas(self.content_frame, width=PHOTO_WIDTH, height=PHOTO_HEIGHT, bg="black",
                                      highlightthickness=0)
        self.photo_canvas.pack(expand=True)

        self.photo_path = PLACEHOLDER_PHOTO
        self.pillow_photo = Image.open(self.photo_path)
        self.resized_photo = ImageOps.contain(self.pillow_photo, (PHOTO_WIDTH, PHOTO_HEIGHT))
        self.display_photo = ImageTk.PhotoImage(self.resized_photo)
        self.photo_canvas.create_image(PHOTO_WIDTH // 2, PHOTO_HEIGHT // 2, image=self.display_photo,
                                       anchor="center")

        # Main Loop
        self.root.mainloop()

    def upload_function(self):
        selected_path = filedialog.askopenfilename(
            title="Select a Photo to Edit",
            filetypes=[("Photos", UPLOAD_BUTTON_EXTENSIONS)],
        )

        # Checking if a file was selected
        if selected_path:
            if self.verify_upload(selected_path):
                # Updating Related Variables/Labels After Selecting a new Photo
                self.pillow_photo.close()
                self.photo_path = selected_path
                self.pillow_photo = Image.open(self.photo_path)
                self.resized_photo = ImageOps.contain(self.pillow_photo, (PHOTO_WIDTH, PHOTO_HEIGHT))
                self.display_photo = ImageTk.PhotoImage(self.resized_photo)
                self.photo_canvas.create_image(PHOTO_WIDTH // 2, PHOTO_HEIGHT // 2, image=self.display_photo,
                                               anchor="center")
            else:
                # Creating a pop-up to show an error
                popup = tk.Toplevel(self.root)
                popup.title("Error")
                popup.geometry("250x75")
                popup.resizable(False, False)
                popup.grab_set() # blocks user from performing other actions unless pop-up is closed
                self.root.eval(f"tk::PlaceWindow {popup} center") # centers popup

                # Error Message
                label = tk.Label(popup, text="Invalid Input! Please try again.", font=("Arial", 12), pady=20)
                label.pack()

                # Closes the Popup after 2000 ms
                popup.after(2000, popup.destroy)

    @staticmethod
    def verify_upload(path):
        if not os.path.exists(path):
            return False

        name, ext = os.path.splitext(path)
        if ext.lower() not in VALID_FILE_EXTENSIONS:
            return False
        return True


if __name__ == "__main__":
    PythonImageEditor()