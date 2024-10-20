# Multi-Screen Wallpaper Splitter

## Project Description
This application is a Multi-Screen Wallpaper Splitter designed to help users easily split and adjust wallpapers for multi-monitor setups. It provides a graphical user interface for loading, splitting, adjusting, and saving wallpaper images across multiple screens.

## Features
- Load and display images
- Automatically detect multi-screen configurations
- Split images horizontally or vertically based on screen layouts
- Adjust split ratios with an interactive slider
- Preview split results in real-time
- Save split images individually

## Installation

### Prerequisites
- Python 3.x
- PIL (Python Imaging Library)
- tkinter
- screeninfo

### Steps
1. Clone this repository or download the source code.
2. Install the required dependencies:
   ```
   pip install pillow tkinter screeninfo
   ```
3. Run the main script:
   ```
   python main.py
   ```

## Usage
1. Launch the application by running `main.py`.
2. Click "Load Image" to select a wallpaper image.
3. Choose "Horizontal Split" or "Vertical Split" based on your screen arrangement.
4. Use the slider to adjust the split ratio if needed.
5. Click "Save Image" to save the split wallpapers.

## File Structure
- `main.py`: Contains the main application logic and GUI.
- `utils/split_wallpaper.py`: Includes utility functions for splitting wallpapers and handling screen information.

## Contributing
Contributions to improve the application are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

## License
[Specify your chosen license here]

## Acknowledgements
This project uses the following open-source libraries:
- PIL (Python Imaging Library)
- tkinter
- screeninfo
