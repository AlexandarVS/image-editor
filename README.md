# PyQt5 Image Editor

## Overview
This is a PyQt5-based Image Editor that allows users to perform various image transformations such as cropping, rotating, mirroring, brightness/contrast/saturation adjustments. The application provides an interactive GUI with intuitive controls.

## Features
- Load and save images in multiple formats (PNG, JPG, BMP, etc.).
- Crop images interactively using a QLabel-based tool.
- Rotate images by 90-degree increments.
- Mirror images horizontally or vertically.
- Adjust brightness, contrast, and saturation using sliders.
- Undo and redo image transformations.
- Reset the image to its original state.

## Installation
### Prerequisites
Ensure you have Python installed, then install the required dependencies:
```sh
pip install -r requirements.txt
```

## Usage
Run the application using:
```sh
python main.py
```

## File Structure
```
project_root/
│── src/
│   ├── image_editor_gui.py   # Main GUI implementation
│   ├── image_processor.py    # Image processing logic
│   ├── image_cropper.py      # Cropping tool implementation
│── tests/
│   ├── test_image_processor.py  # Unit tests
│── main.py  # Entry point
│── requirements.txt  # Dependencies
│── README.md  # This file
```

## Testing
Run the unit tests using:
```sh
pytest tests/
```

## Dependencies
- PyQt5
- OpenCV
- Pillow
- NumPy
- PyTest (for testing)

## License
No License

## Author
Aleksandar Slavov

