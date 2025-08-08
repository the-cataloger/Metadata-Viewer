# Metadata Viewer

## Overview
Metadata Viewer is a Python application designed to extract and display metadata from image files. It provides a graphical user interface (GUI) built with Tkinter, allowing users to open an image, view its metadata, and save the metadata as a text report.

## Features
- Displays basic file metadata (e.g., file name, size, type, and last modified date).
- Extracts EXIF metadata using the `exifread` library.
- Detects ICC profiles embedded in images.
- Extracts XMP metadata (if available).
- Allows saving metadata as a text report.
- Supports multiple image formats: JPG, PNG, TIFF, BMP, GIF, and WebP.

## Requirements
To run the Metadata Viewer application, you need the following Python libraries installed:
- `tkinter` (usually included with Python; for GUI)
- `Pillow` (for image processing)
- `exifread` (for extracting EXIF metadata)

You can install the required libraries using pip:
```bash
pip install Pillow exifread
```

## Installation
1. Clone or download this repository to your local machine.
2. Ensure Python 3.x is installed.
3. Install the required libraries as mentioned above.

## Usage
1. Run the script `Metadata-Viewer3.py`:
   ```bash
   python Metadata-Viewer3.py
   ```
2. Click the **Open Image** button to select an image file.
3. The application will display the image (scaled to fit) and its metadata in the text area.
4. To save the metadata, click the **Save Report** button and choose a location to save the `.txt` file.

## Supported File Formats
- JPG/JPEG
- PNG
- TIFF
- BMP
- GIF
- WebP

## Notes
- Ensure the image file is valid and accessible to avoid errors.
- Some metadata (e.g., EXIF or XMP) may not be available for all images.
- The application requires read access to the image file and write access to save the report.

## Author
The Cataloger  
Email: manuscriptscataloger@gmail.com