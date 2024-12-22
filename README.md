# Py-Cartoonize

Py-Cartoonize is a Python-based image processing project that applies a cartoon effect to images. The program takes images from an input folder, processes them to generate a cartoonized version, and saves the results in an output folder. Additionally, it creates side-by-side comparison images of the original and cartoonized images for easy visualization.

## Features
- Cartoonizes images using:
  - Bilateral filtering for smoothing.
  - Adaptive thresholding for edge detection.
  - K-means clustering for color quantization.
- Automatically processes all images in the input folder.
- Saves both cartoonized images and side-by-side comparison images.
- Supports customizable input and output folders.

## Requirements
- Python 3.x
- OpenCV
- NumPy

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd py-cartoonize
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Place the images to be cartoonized in the `images` folder.
2. Run the program:
   ```bash
   python cartoonizer.py
   ```
3. The cartoonized images will be saved in the `cartoonized` folder, and the side-by-side comparison images will be saved in the `comparisons` folder.

## File Structure
```
py-cartoonize/
├── cartoonizer.py         # Main script for cartoonizing images
├── images/                # Folder for input images
├── cartoonized/           # Folder for cartoonized output images
├── comparisons/           # Folder for side-by-side comparison images
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
```

## How It Works
1. **Preprocessing**:
   - The input image is smoothed using Gaussian and Median blur to reduce noise.
   - A bilateral filter is applied to preserve edges while smoothing colors.

2. **Edge Detection**:
   - The processed image is converted to grayscale.
   - Adaptive thresholding detects edges in localized regions.
   - The resulting edge image is smoothed to minimize harsh transitions.

3. **Color Quantization**:
   - The image is reshaped and processed using K-means clustering for color reduction.
   - A fixed number of color clusters (e.g., 8) is used to create a cartoon-like palette.

4. **Final Output**:
   - The edge mask is blended with the quantized color image to create the cartoon effect.
   - A side-by-side comparison image is generated and saved.

## Example Output
- **Cartoonized Image**: `cartoonized/cartoon_image_name.png`
- **Comparison Image**: `comparisons/comparison_image_name.png`