VeinMapper Image Processing Tool
This project processes raw infrared images to isolate and visualize finger vein patterns. We developed a Python application that applies computer vision techniques to enhance low contrast images, extract vein structures, and map key geometric points. The system runs on a Flask server and renders the analysis in a web browser.

Project Overview
The goal of this code is to transform noisy infrared inputs into clean, visible vein maps. The program reads images from a local directory and passes them through a processing pipeline that enhances contrast, removes background noise, and thins the vein lines to their structural core. We also implemented a custom algorithm to detect specific pixel patterns where lines end or intersect.

Technical Implementation
The code relies on OpenCV for image manipulation and NumPy for matrix operations. The core logic is split into four specific processing steps.

1. Contrast and Enhancement

We use CLAHE (Contrast Limited Adaptive Histogram Equalization) to fix lighting inconsistencies. Since raw infrared images are often dark or uneven, this step locally adjusts intensity in 8x8 pixel grids to make the veins distinct from the skin.

2. Segmentation and Masking

To separate the veins from the background, we apply Adaptive Gaussian Thresholding. This calculates thresholds based on neighboring pixels rather than a global value. We also generate a binary mask using contours to identify the finger shape, ensuring we only process the relevant area and ignore the black borders.

3. Skeletonization

We implemented a custom iterative loop to thin the veins. The code repeatedly erodes the binary image and subtracts the result from the previous step. This process continues until the veins are reduced to a single pixel width, creating a clean "skeleton" of the network.

4. Feature Detection

The system analyzes the skeletonized image to find geometric nodes. We count the neighbors of every white pixel:

Endpoints are pixels with exactly 1 neighbor

Intersections are pixels with 3 or more neighbors

We filter these points using a Euclidean distance check to prevent clustering.

Web Interface
The project uses Flask to serve the results. The backend generates a tiled dashboard that combines the Enhanced, Binary, Skeleton, and Final Map images into a single view. The interface includes API endpoints to fetch dataset statistics and navigation controls to cycle through patient files.

Dataset
We tested the code using the Kaggle Finger Vein Dataset, which provides the necessary infrared samples for calibration.

Source: Kaggle Finger Vein Dataset
