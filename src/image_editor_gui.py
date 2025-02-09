"""
Image Editor GUI using PyQt5.
Allows users to perform various image transformations such as rotating, mirroring,
brightness/contrast adjustments, and more.
"""

import sys

try:
    from PyQt5.QtWidgets import (
        QLabel, QMainWindow, QPushButton, QFileDialog,
        QVBoxLayout, QWidget, QSlider, QHBoxLayout, QComboBox,
        QScrollArea
    )
    from PyQt5.QtGui import QPixmap, QImage
    from PyQt5.QtCore import Qt
except ImportError:
    print("Error: PyQt5 is not installed. Install it using: pip install PyQt5")
    sys.exit(1)

try:
    from image_processor import ImageProcessor
    from image_cropper import CropImageLabel
except ImportError:
    print("Error: Required modules (image_processor, image_cropper) not found.")
    sys.exit(1)

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.processor = ImageProcessor()

        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 1200, 700)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.controls_layout = QVBoxLayout()
        self.layout.addLayout(self.controls_layout)

        self.setup_controls()
        self.setup_image_display()

    def setup_controls(self):
        """Setup the left-side controls (buttons, sliders, etc.)."""
        self.setup_buttons()
        self.setup_rotation_section()
        self.setup_mirror_section()
        self.setup_adjustment_sliders()

    def setup_image_display(self):
        """Set up QLabel for displaying images within a scrollable area."""
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.image_label = CropImageLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: none; background-color: transparent;")
        self.scroll_area.setWidget(self.image_label)

        self.layout.addWidget(self.scroll_area)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

    def setup_buttons(self):
        """Add Load, Save, Undo, Redo, and Reset buttons."""
        button_layout = QVBoxLayout()

        self.load_button = QPushButton("📂 Load Image")
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)

        self.save_button = QPushButton("💾 Save Image")
        self.save_button.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_button)

        self.undo_button = QPushButton("↩️ Undo")
        self.undo_button.clicked.connect(self.undo)
        button_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("↪️ Redo")
        self.redo_button.clicked.connect(self.redo)
        button_layout.addWidget(self.redo_button)

        self.reset_button = QPushButton("🔄 Reset Image")
        self.reset_button.clicked.connect(self.reset_image)
        button_layout.addWidget(self.reset_button)

        self.controls_layout.addLayout(button_layout)

    def setup_rotation_section(self):
        """Set up Rotation button."""
        self.rotate_button = QPushButton("🔄 Rotate 90°")
        self.rotate_button.clicked.connect(self.rotate_image)
        self.controls_layout.addWidget(self.rotate_button)

    def setup_mirror_section(self):
        """Set up Mirror options."""
        mirror_layout = QHBoxLayout()

        self.mirror_dropdown = QComboBox()
        self.mirror_dropdown.addItems(["Horizontal", "Vertical"])
        mirror_layout.addWidget(self.mirror_dropdown)

        self.mirror_button = QPushButton("🔁 Mirror")
        self.mirror_button.clicked.connect(self.mirror_image)
        mirror_layout.addWidget(self.mirror_button)

        self.controls_layout.addLayout(mirror_layout)

    def setup_adjustment_sliders(self):
        """Set up Brightness, Contrast, and Saturation sliders."""
        self.brightness_slider = self.create_slider("🔆 Brightness", self.adjust_brightness)
        self.contrast_slider = self.create_slider("🎛 Contrast", self.adjust_contrast)
        self.saturation_slider = self.create_slider("🎨 Saturation", self.adjust_saturation)

    def create_slider(self, name, function):
        """Helper function to create a slider that saves state only when released."""
        slider_layout = QVBoxLayout()
        slider_label = QLabel(name)
        slider_layout.addWidget(slider_label)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(-100, 100)
        slider.setValue(0)

        slider.sliderPressed.connect(self.save_adjustment_state)

        slider.valueChanged.connect(function)

        slider_layout.addWidget(slider)
        self.controls_layout.addLayout(slider_layout)
        return slider

    def load_image(self):
        """Load an image and remove extra space in the window."""
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                "Open Image",
                                                "", 
                                                "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.processor.load_image(file_path)
            self.display_image()

    def save_image(self):
        """Save the edited image."""
        file_path, _ = QFileDialog.getSaveFileName(self, 
                                                   "Save Image", 
                                                   "", 
                                                   "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.processor.save_image(file_path)

    def rotate_image(self):
        """Rotate the image by 90 degrees."""
        self.processor.rotate_image(90)
        self.display_image()

    def mirror_image(self):
        """Mirror the image based on the dropdown selection."""
        direction = self.mirror_dropdown.currentText().lower()
        self.processor.mirror_image(direction)
        self.display_image()

    def apply_adjustments(self):
        """Applies brightness, contrast, and saturation adjustments cumulatively."""
        if self.processor.transformed_image is None:
            return

        self.processor.image = self.processor.transformed_image

        brightness_factor = self.brightness_slider.value() / 100
        contrast_factor = self.contrast_slider.value() / 100
        saturation_factor = self.saturation_slider.value() / 100

        self.processor.adjust_brightness(brightness_factor)
        self.processor.adjust_contrast(contrast_factor)
        self.processor.adjust_saturation(saturation_factor)

        self.display_image()

    def adjust_brightness(self):
        """Adjust brightness and apply all transformations."""
        self.apply_adjustments()

    def adjust_contrast(self):
        """Adjust contrast and apply all transformations."""
        self.apply_adjustments()

    def adjust_saturation(self):
        """Adjust saturation and apply all transformations."""
        self.apply_adjustments()

    def reset_image(self):
        """Reset the image to its original state."""
        self.processor.reset_image()
        self.saturation_slider.setValue(0)
        self.contrast_slider.setValue(0)
        self.brightness_slider.setValue(0)
        self.display_image()

    def display_image(self):
        """Update the QLabel with the current image."""
        if self.processor.image:
            qimage = self.pil_to_qimage(self.processor.image)
            pixmap = QPixmap.fromImage(qimage)

            pixmap = pixmap.scaled(
                self.scroll_area.size(),
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation)

            self.image_label.set_image(self.processor.image)
            self.image_label.setPixmap(pixmap)

            self.scroll_area.setFixedSize(900, 700)
            self.scroll_area.setWidgetResizable(True)

    def undo(self):
        """Perform an undo operation."""
        new_image = self.processor.undo()
        if new_image:
            self.display_image()

    def redo(self):
        """Perform a redo operation."""
        new_image = self.processor.redo()
        if new_image:
            self.display_image()

    def save_adjustment_state(self):
        """Save the state only once when the slider is first clicked."""
        if self.processor and self.processor.image:
            self.processor.save_state()

    def pil_to_qimage(self, pil_image):
        """Convert a PIL image to QImage."""
        img = pil_image.convert("RGBA")
        data = img.tobytes("raw", "RGBA")
        return QImage(data, img.width, img.height, QImage.Format_RGBA8888)
