import cv2
import os
import numpy as np

def cartoonize_image(input_path, output_path, comparison_output_path):
    """
    Reads an image from the input path, applies a cartoon effect, and saves the result to the output path.
    Also generates a side-by-side comparison of the original and cartoonized image.
    """
    # Read the original image
    image = cv2.imread(input_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {input_path}")

    img_gb = cv2.GaussianBlur(image, (7, 7), 0)
    img_mb = cv2.medianBlur(img_gb, 5)
    img_bf = cv2.bilateralFilter(img_mb, 5, 80, 80)

    # Use the laplace filter to detect edges
    img_lp_im = cv2.Laplacian(image, cv2.CV_8U, ksize=5)
    img_lp_gb = cv2.Laplacian(img_gb, cv2.CV_8U, ksize=5)
    img_lp_mb = cv2.Laplacian(img_mb, cv2.CV_8U, ksize=5)
    img_lp_al = cv2.Laplacian(img_bf, cv2.CV_8U, ksize=5)

    # Convert the image to greyscale (1D)
    img_lp_im_grey = cv2.cvtColor(img_lp_im, cv2.COLOR_BGR2GRAY)
    img_lp_gb_grey = cv2.cvtColor(img_lp_gb, cv2.COLOR_BGR2GRAY)
    img_lp_mb_grey = cv2.cvtColor(img_lp_mb, cv2.COLOR_BGR2GRAY)
    img_lp_al_grey = cv2.cvtColor(img_lp_al, cv2.COLOR_BGR2GRAY)

    # Manual image thresholding
    _, EdgeImage = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Remove some additional noise
    blur_im = cv2.GaussianBlur(img_lp_im_grey, (5, 5), 0)
    blur_gb = cv2.GaussianBlur(img_lp_gb_grey, (5, 5), 0)
    blur_mb = cv2.GaussianBlur(img_lp_mb_grey, (5, 5), 0)
    blur_al = cv2.GaussianBlur(img_lp_al_grey, (5, 5), 0)
    # Apply a threshold (Otsu)
    _, tresh_im = cv2.threshold(blur_im, 245, 255,cv2.THRESH_BINARY +  cv2.THRESH_OTSU)
    _, tresh_gb = cv2.threshold(blur_gb, 245, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, tresh_mb = cv2.threshold(blur_mb, 245, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, tresh_al = cv2.threshold(blur_al, 245, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the black and the white
    inverted_original = cv2.subtract(255, tresh_im)
    inverted_GaussianBlur = cv2.subtract(255, tresh_gb)
    inverted_MedianBlur = cv2.subtract(255, tresh_mb)
    inverted_Bilateral = cv2.subtract(255, tresh_al)

    # Reshape the image
    img_reshaped = image.reshape((-1,3))
    # convert to np.float32
    img_reshaped = np.float32(img_reshaped)
    # Set the Kmeans criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    # Set the amount of K (colors)
    K = 8
    # Apply Kmeans
    _, label, center = cv2.kmeans(img_reshaped, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Covert it back to np.int8
    center = np.uint8(center)
    res = center[label.flatten()]
    # Reshape it back to an image
    img_Kmeans = res.reshape((image.shape))

    # Reduce the colors of the original image
    div = 64
    img_bins = image // div * div + div // 2

    # Convert the mask image back to color 
    inverted_Bilateral = cv2.cvtColor(inverted_Bilateral, cv2.COLOR_GRAY2RGB)
    # Combine the edge image and the binned image
    cartoon_Bilateral = cv2.bitwise_and(inverted_Bilateral, img_bins)
    # Save the cartoonized image
    cv2.imwrite(output_path, cartoon_Bilateral)
    print(f"Cartoonized image saved at {output_path}")

    # Combine the original and cartoonized images side by side for comparison
    comparison_image = cv2.hconcat([image, cartoon_Bilateral])

    # Save the comparison image
    cv2.imwrite(comparison_output_path, comparison_image)
    print(f"Comparison image saved at {comparison_output_path}")

if __name__ == "__main__":
    # Input and output folder paths
    input_folder = "images"
    output_folder = "cartoonized"
    comparison_folder = "comparisons"

    # Ensure the output folders exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(comparison_folder, exist_ok=True)

    # Process each image in the input folder
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, f"cartoon_{file_name}")
        comparison_output_path = os.path.join(comparison_folder, f"comparison_{file_name}")
        
        try:
            cartoonize_image(input_path, output_path, comparison_output_path)
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")
