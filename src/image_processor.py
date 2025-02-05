"""
This module provides image loading and saving functionality using the PIL library.
"""

import os
from PIL import Image
from PIL import ImageEnhance

class ImageProcessor:
    """Class to handle image processing tasks such as loading and saving images."""

    def __init__(self):
        """Initialize the ImageProcessor with no image loaded."""
        self.image = None
        self.file_path = None
        self.original_image = None

    def load_image(self, file_path):
        """
        Loads an image from a given file path.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found!")

        self.image = Image.open(file_path)
        self.original_image = self.image.copy()
        self.file_path = file_path
        return self.image

    def save_image(self, save_path, file_format=None):
        """
        Saves the currently loaded image to the specified file path in the given format.
        """
        if self.image is None:
            raise ValueError("No image loaded to save!")

        file_format = file_format.upper() if file_format else self.image.format
        self.image.save(save_path, format=file_format)

    def reset_image(self):
        """Resets image to its original state."""
        if self.original_image is None:
            raise ValueError("No original image to reset!")
        
        self.image = self.original_image.copy()
        print("✅ Image reset to original state.")

    def resize_image(self, new_width, new_height):
        """Resizes the image to the specified dimensions."""
        if self.image is None:
            raise ValueError("No image loaded to resize!")

        self.image = self.image.resize((new_width, new_height))
        return self.image

    def crop_image(self, left, top, right, bottom):
        """Crops the image to the specified box dimensions."""
        if self.image is None:
            raise ValueError("No image loaded to crop!")

        self.image = self.image.crop((left, top, right, bottom))
        return self.image

    def rotate_image(self, degrees):
        """Rotates the image by the given number of degrees."""
        if self.image is None:
            raise ValueError("No image loaded to rotate!")

        self.image = self.image.rotate(degrees, expand=True)
        return self.image

    def mirror_image(self, direction="horizontal"):
        """Flips the image either horizontally or vertically."""
        if self.image is None:
            raise ValueError("No image loaded to mirror!")

        if direction.lower() == "horizontal":
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT) # pylint: disable=no-member
        elif direction.lower() == "vertical":
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM) # pylint: disable=no-member
        else:
            raise ValueError("Invalid direction! Use 'horizontal' or 'vertical'.")

        return self.image

    def adjust_brightness(self, factor):
        """Adjusts image brightness. Factor > 1 increases brightness, factor < 1 decreases."""
        if self.image is None:
            raise ValueError("No image loaded to adjust brightness!")

        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self.image

    def adjust_contrast(self, factor):
        """Adjusts image contrast. Factor > 1 increases contrast, factor < 1 decreases."""
        if self.image is None:
            raise ValueError("No image loaded to adjust contrast!")

        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self.image

    def adjust_saturation(self, factor):
        """Adjusts image saturation. Factor > 1 increases saturation, factor < 1 decreases."""
        if self.image is None:
            raise ValueError("No image loaded to adjust saturation!")

        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self.image

    def convert_to_black_and_white(self):
        """Converts image to grayscale (Black & White)."""
        if self.image is None:
            raise ValueError("No image loaded to convert!")

        self.image = self.original_image.copy()
        self.image = self.image.convert("L")
        return self.image
