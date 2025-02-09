import cv2
import numpy as np
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect
from PIL import Image


class CropImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.mouse_pressed = False
        self.image = None
        self.cv_image = None
        self.parent_window = parent

    def set_image(self, image):
        """Set and display the image, converting PIL to OpenCV format."""
        self.image = image
        self.cv_image = np.array(image.convert("RGB"))[:, :, ::-1]
        self.update_display()

    def update_display(self):
        """Update QLabel with the current image."""
        if self.cv_image is not None:
            qimage = self.cv2_to_qimage(self.cv_image)
            pixmap = QPixmap.fromImage(qimage)
            self.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        """Start cropping when the left mouse button is pressed."""
        if self.cv_image is not None:
            self.mouse_pressed = True
            self.start_x, self.start_y = event.x(), event.y()
            self.end_x, self.end_y = self.start_x, self.start_y
            self.update()

    def mouseMoveEvent(self, event):
        """Draw the selection box while the mouse is moving."""
        if self.mouse_pressed:
            self.end_x, self.end_y = event.x(), event.y()
            self.update()

    def mouseReleaseEvent(self, event):
        """Apply cropping when the left mouse button is released."""
        if self.mouse_pressed:
            self.mouse_pressed = False
            self.end_x, self.end_y = event.x(), event.y()
            self.apply_crop()
            self.update()

    def apply_crop(self):
        """Perform OpenCV-based cropping."""
        if self.cv_image is None:
            return

        if self.start_x > self.end_x:
            self.start_x, self.end_x = self.end_x, self.start_x
        if self.start_y > self.end_y:
            self.start_y, self.end_y = self.end_y, self.start_y

        label_width, label_height = self.width(), self.height()
        img_height, img_width, _ = self.cv_image.shape

        left = int((self.start_x / label_width) * img_width)
        right = int((self.end_x / label_width) * img_width)
        top = int((self.start_y / label_height) * img_height)
        bottom = int((self.end_y / label_height) * img_height)

        if right - left > 5 and bottom - top > 5:
            self.cv_image = self.cv_image[top:bottom, left:right]
            self.image = Image.fromarray(cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB))
            self.update_display()
            self.parent_window.processor.transformed_image = self.image.copy()
            self.parent_window.processor.image = self.image.copy()

    def paintEvent(self, event):
        """Draw the selection rectangle while cropping."""
        super().paintEvent(event)
        if self.mouse_pressed:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.green, 2, Qt.DashLine))
            rect = QRect(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y)
            painter.drawRect(rect)

    def cv2_to_qimage(self, cv_image):
        """Convert OpenCV image (BGR) to QImage (RGB)."""
        height, width, channel = cv_image.shape
        bytes_per_line = width * channel
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        qimage = QImage(rgb_image.data.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888)
        return qimage
