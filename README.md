# BoldBrush SVG2EPS

This tool provides a graphical user interface to convert SVG files to both EPS and JPEG formats. It leverages Inkscape for the core conversion process and Pillow for image manipulation.
# Developed By Wahab Muhammad
## Prerequisites

1. Python 3.x (includes tkinter by default)
2. Inkscape (must be installed separately and its executable accessible by the system)
3. Pillow Python library

### Installing Prerequisites

1. **Python**: 
   - Download and install from [python.org](https://www.python.org/downloads/)
   - Make sure to check "tcl/tk and IDLE" during installation to include tkinter

2. **Inkscape**: 
   - Download from [inkscape.org](https://inkscape.org/release/)
   - Ensure the Inkscape executable (`inkscape.exe` on Windows) is in your system's PATH, or update the `inkscape_path` variable in the script (`eps_converter.py`) to the correct location.

3. **Pillow**: 
   - Install using pip. Navigate to the project directory in your terminal and run:
     ```bash
     pip install -r requirements.txt
     ```

## Installation

1. Clone or download this repository

## Usage

1. Run the script from your terminal within the project directory:
   ```bash
   python eps_converter.py
   ```
   (If `python` command doesn't work, try `python3`)

2. In the GUI:
   - Click "Add Files" to select the SVG files you want to convert.
   - Click "Browse" to select the output directory where converted EPS and JPEG files will be saved.
   - Click "Convert Files" to start the conversion process.
   - Monitor the progress in the text area.

## Features

- Converts SVG files to EPS format
- Converts SVG files to JPEG format
- User-friendly graphical interface
- Progress monitoring
- Error handling and reporting
- Multi-threaded conversion process

## Notes

- The script will create both EPS and JPEG versions for each selected SVG file.
- Output files will have the same base name as the input file but with `.eps` and `.jpg` extensions.
- JPEG conversion settings are optimized for platforms like Pinterest/Instagram (quality 75, optimized).
- Inkscape is required and must be installed separately.
