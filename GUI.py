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
SIDEBAR_BUTTON_SIZE = 64
SIDEBAR_WIDTH: int = 88
NAVBAR_HEIGHT: int = 64
PLACEHOLDER_PHOTO: str = "assets/placeholder-photo.png"
VALID_FILE_EXTENSIONS: dict[str, int] = {".png": 0, ".pgm": 0, ".ppm": 0, ".gif": 0}

# Formatting a string for filedialog option
UPLOAD_BUTTON_EXTENSIONS: str = "*.png *.pgm *.ppm *.gif"

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
        self.navbar_frame = tk.Frame(self.root, bg=ACCENT_COLOR)
        self.navbar_frame.pack(side="top", ipady=8, fill="x")

        self.upload_button = tk.Button(self.navbar_frame, text="upload", command=self.update_upload_path)
        self.upload_button.pack(side="left", padx=16, pady=20)

        self.save_button = tk.Button(self.navbar_frame, text="save", command=self.save_photo)
        self.save_button.pack(side="left", pady=20)

        # SideBar
        self.sidebar_frame = tk.Frame(self.root, bg=PRIMARY_COLOR)
        self.sidebar_frame.pack(side="left", fill="y", ipadx=16)

        self.rotate_btn = tk.Button(self.sidebar_frame, bg=ACCENT_COLOR, text="R", command=self.rotate_image)
        self.rotate_btn.pack(padx=16)

        self.vertical_flip_btn = tk.Button(self.sidebar_frame, bg=ACCENT_COLOR, text="V", command=self.vertical_flip)
        self.vertical_flip_btn.pack(padx=16)

        self.horizontal_flip_btn = tk.Button(self.sidebar_frame, bg=ACCENT_COLOR, text="H", command=self.horizontal_flip)
        self.horizontal_flip_btn.pack(padx=16)

        # Content Area
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Photo
        self.photo_canvas = tk.Canvas(self.content_frame, width=PHOTO_WIDTH, height=PHOTO_HEIGHT, highlightthickness=0)
        self.photo_canvas.pack(expand=True)

        self.photo_path = PLACEHOLDER_PHOTO
        self.photo_name = "placeholder-photo"
        self.photo_extension = ".png"
        self.pillow_photo = Image.open(self.photo_path)
        self.resized_photo = ImageOps.contain(self.pillow_photo, (PHOTO_WIDTH, PHOTO_HEIGHT))
        self.display_photo = ImageTk.PhotoImage(self.resized_photo)
        self.photo_id = self.photo_canvas.create_image(PHOTO_WIDTH // 2, PHOTO_HEIGHT // 2,
                                                       image=self.display_photo, anchor="center")

        # Main Loop
        self.root.mainloop()

    def update_display_photo(self):
        self.resized_photo = ImageOps.contain(self.pillow_photo, (PHOTO_WIDTH, PHOTO_HEIGHT))
        self.display_photo = ImageTk.PhotoImage(self.resized_photo)
        self.photo_canvas.itemconfig(self.photo_id, image=self.display_photo)

    @staticmethod
    def get_upload_path() -> str:
        return filedialog.askopenfilename(
            title="Select a Photo to Edit",
            filetypes=[("Photos", UPLOAD_BUTTON_EXTENSIONS)],
        )

    def update_upload_path(self) -> bool:
        selected_path = self.get_upload_path()

        # Checking if a file was selected
        if selected_path:
            if self.verify_image_path(selected_path):
                # Updating Related Variables/Labels After Selecting a new Photo
                self.pillow_photo.close()
                self.photo_path = selected_path
                self.photo_name, self.photo_extension = os.path.splitext(os.path.basename(self.photo_path))
                self.pillow_photo = Image.open(self.photo_path)
                self.update_display_photo()
                return True
            else:
                self.create_popup(
                    "Error!",
                    "Invalid Input Image! Please try uploading again.",
                    (400, 100)
                )
        return False

    def get_output_path(self) -> str:
        return filedialog.asksaveasfilename(
            title="Save Photo",
            initialfile=self.photo_name,
            defaultextension=self.photo_extension,
            filetypes=[("Select an Output Folder", "/")]
        )

    def save_photo(self) -> bool:
        if self.photo_path == PLACEHOLDER_PHOTO:
            self.create_popup(
                "Error!",
                "Error! You have not uploaded an image to be saved\nPlease upload an image before saving.",
                (400, 100)
            )
            return False

        # Checking if an output path is selected
        output_path = self.get_output_path()
        if output_path:
            output_name, output_ext = os.path.splitext(output_path)
            if output_ext.lower() not in VALID_FILE_EXTENSIONS:
                self.create_popup(
                    "Error!",
                    f"Error! Failed to Save {self.photo_name}.\nPlease try a different file extension.",
                    (450, 100)
                )
                return False

            try:
                self.pillow_photo.save(output_path)
                self.create_popup(
                    "Success!",
                    f"Image was successfully saved at\n{output_path}.",
                    (400, 100)
                )
                return True
            except:
                self.create_popup(
                    "Error!",
                    f"Error! Failed to Save {self.photo_name}.\nPlease try again.",
                    (400, 100)
                )
        return False

    @staticmethod
    def verify_image_path(path: str) -> bool:
        if not os.path.exists(path):
            return False

        name, ext = os.path.splitext(path)
        if ext.lower() not in VALID_FILE_EXTENSIONS:
            return False
        return True

    def create_popup(self,  title: str, message: str, size: tuple[int, int]) -> None:
        # Creating a pop-up to show an error
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(f"{size[0]}x{size[1]}")
        popup.resizable(False, False)
        popup.grab_set()  # blocks user from performing other actions unless pop-up is closed
        self.root.eval(f"tk::PlaceWindow {popup} center")  # centers popup

        # Error Message
        label = tk.Label(popup, text=message, font=("Arial", 12), pady=20)
        label.pack()

        close_btn = tk.Button(popup, text="Close", width=7, height=2, command=popup.destroy, bg=PRIMARY_COLOR)
        close_btn.pack()

    # Image Functions
    def rotate_image(self):
        self.pillow_photo = image_functions.rotate_image(self.pillow_photo, 90)
        self.update_display_photo()

    def vertical_flip(self):
        self.pillow_photo = image_functions.vertical_flip(self.pillow_photo)
        self.update_display_photo()

    def horizontal_flip(self):
        self.pillow_photo = image_functions.horizontal_flip(self.pillow_photo)
        self.update_display_photo()

if __name__ == "__main__":
    PythonImageEditor()