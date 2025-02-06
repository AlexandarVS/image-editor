import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, 
                             QVBoxLayout, QWidget, QSlider, QHBoxLayout, QComboBox, 
                             QSpinBox, QMessageBox, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRect
from image_processor import ImageProcessor
from image_cropper import CropImageLabel

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize image processor
        self.processor = ImageProcessor()

        # Set up the main window
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 900, 700)

        # Main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Setup UI components
        self.setup_image_display()
        self.setup_buttons()
        self.setup_crop_section()
        self.setup_rotation_section()
        self.setup_mirror_section()
        self.setup_adjustment_sliders()

    def setup_image_display(self):
        """Set up QLabel for displaying images without extra spacing."""
        self.image_label = CropImageLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: none; background-color: transparent;")  # Removes extra space
        self.layout.addWidget(self.image_label)

    def setup_buttons(self):
        """Set up Load and Save buttons."""
        button_layout = QHBoxLayout()

        self.load_button = QPushButton("📂 Load Image")
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)

        self.save_button = QPushButton("💾 Save Image")
        self.save_button.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_button)

        self.layout.addLayout(button_layout)


    def setup_crop_section(self):
        """Set up Crop button."""
        self.crop_button = QPushButton("✂️ Crop (Drag on Image)")
        self.crop_button.clicked.connect(self.start_cropping)
        self.layout.addWidget(self.crop_button)

    def setup_rotation_section(self):
        """Set up Rotation button."""
        self.rotate_button = QPushButton("🔄 Rotate 90°")
        self.rotate_button.clicked.connect(self.rotate_image)
        self.layout.addWidget(self.rotate_button)

    def setup_mirror_section(self):
        """Set up Mirror options."""
        mirror_layout = QHBoxLayout()

        self.mirror_dropdown = QComboBox()
        self.mirror_dropdown.addItems(["Horizontal", "Vertical"])
        mirror_layout.addWidget(self.mirror_dropdown)

        self.mirror_button = QPushButton("🔁 Mirror")
        self.mirror_button.clicked.connect(self.mirror_image)
        mirror_layout.addWidget(self.mirror_button)

        self.layout.addLayout(mirror_layout)

    def setup_adjustment_sliders(self):
        """Set up Brightness, Contrast, and Saturation sliders."""
        self.brightness_slider = self.create_slider("🔆 Brightness", self.adjust_brightness)
        self.contrast_slider = self.create_slider("🎛 Contrast", self.adjust_contrast)
        self.saturation_slider = self.create_slider("🎨 Saturation", self.adjust_saturation)

        # Black & White Button
        self.bw_button = QPushButton("⚫ Convert to Black & White")
        self.bw_button.clicked.connect(self.convert_to_bw)
        self.layout.addWidget(self.bw_button)

    def create_slider(self, name, function):
        """Helper function to create a slider."""
        slider_layout = QVBoxLayout()
        slider_label = QLabel(name)
        slider_layout.addWidget(slider_label)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(-100, 100)
        slider.setValue(0)
        slider.valueChanged.connect(function)
        slider_layout.addWidget(slider)

        self.layout.addLayout(slider_layout)
        return slider

    def load_image(self):
        """Load an image and remove extra space in the window."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.processor.load_image(file_path)
            self.display_image()

            # Resize window to fit image perfectly
            self.adjustSize()

    def save_image(self):
        """Save the edited image."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.processor.save_image(file_path)


    def start_cropping(self):
        """Enable cropping mode and provide instructions."""
        if self.processor.image:
            QMessageBox.information(self, "Crop Mode", "Click and drag on the image to select the crop area.")

    def rotate_image(self):
        """Rotate the image by 90 degrees."""
        self.processor.rotate_image(90)
        self.display_image()

    def mirror_image(self):
        """Mirror the image based on the dropdown selection."""
        direction = self.mirror_dropdown.currentText().lower()
        self.processor.mirror_image(direction)
        self.display_image()

    def adjust_brightness(self):
        """Adjust brightness without affecting image scaling."""
        self.processor.adjust_brightness(self.brightness_slider.value() / 100)
        self.display_image()

    def adjust_contrast(self):
        """Adjust contrast without affecting image scaling."""
        self.processor.adjust_contrast(self.contrast_slider.value() / 100)
        self.display_image()

    def adjust_saturation(self):
        """Adjust saturation without affecting image scaling."""
        self.processor.adjust_saturation(self.saturation_slider.value() / 100)
        self.display_image()

    def convert_to_bw(self):
        """Convert image to black and white."""
        self.processor.convert_to_black_and_white()
        self.display_image()

    def display_image(self):
        """Update the QLabel with the current image"""
        if self.processor.image:
            qimage = self.pil_to_qimage(self.processor.image)
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.set_image(self.processor.image)
            self.image_label.setPixmap(pixmap)
            img_width, img_height = self.processor.image.size
            self.image_label.setFixedSize(img_width, img_height)
           
            
    def pil_to_qimage(self, pil_image):
        """Convert a PIL image to QImage."""
        img = pil_image.convert("RGBA")
        data = img.tobytes("raw", "RGBA")
        return QImage(data, img.width, img.height, QImage.Format_RGBA8888)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec_())
