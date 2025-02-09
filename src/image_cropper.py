"""
This module provides a QLabel-based image cropping tool for PyQt5.

It allows users to interactively crop images using mouse events.
"""

# pylint: disable=I1101, E1101

import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image


class CropImageLabel(QtWidgets.QLabel):
    """
    A QLabel subclass for cropping images interactively.

    Attributes:
        crop_coords (dict): Dictionary containing start_x, start_y, end_x, end_y.
        mouse_pressed (bool): Whether the mouse is currently pressed.
        image (PIL.Image): The current image.
        cv_image (numpy.ndarray): OpenCV representation of the image.
        parent_window (QWidget): The parent window containing this widget.
    """

    def __init__(self, parent=None):
        """
        Initialize the CropImageLabel instance.
        """
        super().__init__(parent)
        self.crop_coords = {'start_x': 0, 'start_y': 0, 'end_x': 0, 'end_y': 0}
        self.mouse_pressed = False
        self.image = None
        self.cv_image = None
        self.parent_window = parent

        setattr(self, "mousePressEvent", self.mouse_press_event)
        setattr(self, "mouseMoveEvent", self.mouse_move_event)
        setattr(self, "mouseReleaseEvent", self.mouse_release_event)
        setattr(self, "paintEvent", self.paint_event)


    def set_image(self, image):
        """
        Set and display the image, converting PIL to OpenCV format.

        Args:
            image (PIL.Image): The image to display.
        """
        self.image = image
        self.cv_image = np.array(image.convert("RGB"))[:, :, ::-1]
        self.update_display()

    def update_display(self):
        """
        Update QLabel with the current image.
        """
        if self.cv_image is not None:
            qimage = self.cv2_to_qimage(self.cv_image)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.setPixmap(pixmap.scaled(
                self.width(), self.height(),
                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            ))

    def mouse_press_event(self, event):
        """
        Start cropping when the left mouse button is pressed.

        Args:
            event (QMouseEvent): Mouse press event.
        """
        if self.cv_image is not None:
            self.mouse_pressed = True
            self.crop_coords["start_x"], self.crop_coords["start_y"] = event.x(), event.y()
            self.crop_coords["end_x"], self.crop_coords["end_y"] = event.x(), event.y()
            self.update()

    def mouse_move_event(self, event):
        """
        Draw the selection box while the mouse is moving.

        Args:
            event (QMouseEvent): Mouse move event.
        """
        if self.mouse_pressed:
            self.crop_coords["end_x"], self.crop_coords["end_y"] = event.x(), event.y()
            self.update()

    def mouse_release_event(self, event):
        """
        Apply cropping when the left mouse button is released.

        Args:
            event (QMouseEvent): Mouse release event.
        """
        if self.mouse_pressed:
            self.mouse_pressed = False
            self.crop_coords["end_x"], self.crop_coords["end_y"] = event.x(), event.y()
            self.apply_crop()
            self.update()

    def apply_crop(self):
        """
        Perform OpenCV-based cropping.
        """
        if self.cv_image is None:
            return

        start_x, start_y = self.crop_coords["start_x"], self.crop_coords["start_y"]
        end_x, end_y = self.crop_coords["end_x"], self.crop_coords["end_y"]

        if start_x > end_x:
            start_x, end_x = end_x, start_x
        if start_y > end_y:
            start_y, end_y = end_y, start_y

        label_width, label_height = self.width(), self.height()
        img_height, img_width, _ = self.cv_image.shape

        left = int((start_x / label_width) * img_width)
        right = int((end_x / label_width) * img_width)
        top = int((start_y / label_height) * img_height)
        bottom = int((end_y / label_height) * img_height)

        if right - left > 5 and bottom - top > 5:
            if self.parent_window:
                self.parent_window.processor.save_state()

            self.cv_image = self.cv_image[top:bottom, left:right]
            if hasattr(cv2, "cvtColor") and hasattr(cv2, "COLOR_BGR2RGB"):
                self.image = Image.fromarray(cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB))

            self.update_display()

            if self.parent_window:
                self.parent_window.processor.transformed_image = self.image.copy()
                self.parent_window.processor.image = self.image.copy()

    def paint_event(self, event):
        """
        Draw the selection rectangle while cropping.

        Args:
            event (QPaintEvent): Paint event.
        """
        super().paintEvent(event)
        if self.mouse_pressed:
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.green, 2, QtCore.Qt.DashLine))
            rect = QtCore.QRect(self.crop_coords["start_x"], self.crop_coords["start_y"],
                                self.crop_coords["end_x"] - self.crop_coords["start_x"],
                                self.crop_coords["end_y"] - self.crop_coords["start_y"])
            painter.drawRect(rect)

    def cv2_to_qimage(self, cv_image):
        """
        Convert OpenCV image (BGR) to QImage (RGB).

        Args:
            cv_image (numpy.ndarray): OpenCV image.

        Returns:
            QtGui.QImage: Converted QImage.
        """
        height, width, channel = cv_image.shape
        bytes_per_line = width * channel
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        qimage = QtGui.QImage(
            rgb_image.data.tobytes(),
            width,
            height,
            bytes_per_line,
            QtGui.QImage.Format_RGB888
        )
        return qimage
