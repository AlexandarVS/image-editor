"""
Unit tests for the ImageProcessor class in src.image_loader.
"""
# pylint: disable=import-error
import os
from PIL import Image
from src.image_processor import ImageProcessor

def test_load_image():
    """
    Test loading an image to ensure it is correctly opened and its dimensions match.
    """
    processor = ImageProcessor()

    img = Image.new("RGB", (100, 100), color="red")
    test_path = "tst/test_image.jpg"
    img.save(test_path)

    loaded_img = processor.load_image(test_path)
    assert loaded_img is not None
    assert loaded_img.size == (100, 100)

    loaded_img.close()

    os.remove(test_path)

def test_save_image():
    """
    Test saving an image and ensure the file is created correctly.
    """
    processor = ImageProcessor()

    processor.image = Image.new("RGB", (50, 50), color="blue")
    test_save_path = "tst/saved_image.png"

    processor.save_image(test_save_path, file_format="PNG")

    assert os.path.exists(test_save_path)
    os.remove(test_save_path)

def test_resize_image():
    """Test image resizing to ensure new dimensions are correct."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (200, 200), color="red")

    processor.resize_image(100, 50)
    assert processor.image.size == (100, 50)

def test_crop_image():
    """Test cropping an image."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (200, 200), color="red")

    processor.crop_image(50, 50, 150, 150)
    assert processor.image.size == (100, 100)

def test_rotate_image():
    """Test rotating an image."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (100, 200), color="blue")

    processor.rotate_image(90)
    assert processor.image.size == (200, 100)

def test_mirror_image():
    """Test mirroring an image."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (100, 100), color="green")

    original_pixels = processor.image.load()[0, 0]

    processor.mirror_image("horizontal")
    mirrored_pixels = processor.image.load()[99, 0]

    assert original_pixels == mirrored_pixels

def test_adjust_brightness():
    """Test brightness adjustment."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (100, 100), color="gray")

    processor.adjust_brightness(1.5)  # Increase brightness
    assert processor.image is not None

def test_adjust_contrast():
    """Test contrast adjustment."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (100, 100), color="gray")

    processor.adjust_contrast(0.5)  # Reduce contrast
    assert processor.image is not None

def test_adjust_saturation():
    """Test saturation adjustment."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (100, 100), color="gray")

    processor.adjust_saturation(2.0)  # Increase saturation
    assert processor.image is not None

def test_convert_to_black_and_white():
    """Test black and white conversion."""
    processor = ImageProcessor()
    processor.image = Image.new("RGB", (100, 100), color="gray")

    processor.convert_to_black_and_white()
    assert processor.image.mode == "L"  # 'L' mode means grayscale
