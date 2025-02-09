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
        self.transformed_image = None
        self.undo_stack = []
        self.redo_stack = []

    def load_image(self, file_path):
        """
        Loads an image from a given file path.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found!")

        self.image = Image.open(file_path)
        self.original_image = self.image.copy()
        self.transformed_image = self.image.copy()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.file_path = file_path
        return self.image

    def save_state(self):
        """Save the current state to the undo stack before making a change."""
        if self.image:
            self.undo_stack.append(self.image.copy())
            self.redo_stack.clear()

    def undo(self):
        """Revert to the previous state if available."""
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.transformed_image = self.image.copy()
            return self.image
        return None

    def redo(self):
        """Reapply the last undone change if available."""
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.transformed_image = self.image.copy()
            return self.image
        return None

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
        self.transformed_image = self.original_image.copy()
        print("✅ Image reset to original state.")

    def rotate_image(self, degrees):
        """Rotates the image by the given number of degrees."""
        if self.image is None:
            raise ValueError("No image loaded to rotate!")

        self.save_state()
        self.image = self.image.rotate(degrees, expand=True)
        self.transformed_image = self.image
        return self.image

    def mirror_image(self, direction="horizontal"):
        """Flips the image either horizontally or vertically."""
        if self.image is None:
            raise ValueError("No image loaded to mirror!")

        self.save_state()
        if direction.lower() == "horizontal":
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)  # pylint: disable=no-member
        elif direction.lower() == "vertical":
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)  # pylint: disable=no-member
        else:
            raise ValueError("Invalid direction! Use 'horizontal' or 'vertical'.")

        self.transformed_image = self.image
        return self.image

    def adjust_brightness(self, factor):
        """Adjusts image brightness. Factor > 1 increases brightness, factor < 1 decreases."""
        if self.image is None:
            raise ValueError("No image loaded to adjust brightness!")
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1 + factor)
        return self.image

    def adjust_contrast(self, factor):
        """Adjusts image contrast. Factor > 1 increases contrast, factor < 1 decreases."""
        if self.image is None:
            raise ValueError("No image loaded to adjust contrast!")
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(1 + factor)
        return self.image

    def adjust_saturation(self, factor):
        """Adjusts image saturation. Factor > 1 increases saturation, factor < 1 decreases."""
        if self.image is None:
            raise ValueError("No image loaded to adjust saturation!")
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(1 + factor)
        return self.image
