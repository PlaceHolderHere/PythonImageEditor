from PIL import ImageFilter


def gray_scale(image):
    return image.convert("L")


def edge_detection(image):
    return image.filter(ImageFilter.FIND_EDGES)


def vertical_flip(image):
    return image.transpose(1)


def horizontal_flip(image):
    return image.transpose(0)


def blur_image(image, intensity: float):  # Base Level is 2
    return image.filter(ImageFilter.GaussianBlur(radius=intensity))


def rotate_image(image, angle):
    return image.rotate(angle, expand=True)
