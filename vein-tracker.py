import cv2 #OpenCV for video capture and display
import os






# -- Dataset Setup -- 
dataset_path = r"C:\Users\dagab\Desktop\vein-mapper\Finger Vein Database\002\left"  # Path to the dataset directory

try:
    file_list = os.listdir(dataset_path) # Getting a list of diles in dataset directo
    images = [f for f in file_list if f.endswith(('.bmp', '.png', '.jpg'))] # Image files and only keeps files with vaild image extentsions
    print(f"Found {len(images)} images in the dataset.") # Display total inages found 
    print("First image name:", images[0]) # Display name of first letter smaple 
except FileNotFoundError: # Handles case where folder path not exists
    print("Error: The folder path is wrong. Check the path in 'dataset_path'")

# -- Processing each image in dataset -- 
# Loop through each image filename in filterd images list 
for image_file in images: 
    full_path = os.path.join(dataset_path, image_file) # Construct comeplte file path by joining directory path and filename

    frame = cv2.imread(full_path) # Reads image file from disk into memory as numpy array
    
    # Checking if image failed to load
    if frame is None: 
        print(f"Error loading image: {full_path}")
        continue # Skips to next image in the loop 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the image to greyscale
    
    # -- Enhance image contrast --
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) # Creating a clahen (Contrast limited adaptive histogram equalization) object 
    enhanced = clahe.apply(gray)

    #now we add adaptive thresholding
    #we make the veins pure white and then use gaussian blur to smooth the image

    #change block size and c value respectively to adjust vein visibility. block size is basically for the noise and if vein broken or invisible lower c value. if too much noise increase block size
    veins = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 3)
    
    # add masking cuz its detecting outside the finger area too
    #tweak second parameter if it cust off too mcuh of finger or includes too much background
    _, finger_mask = cv2.threshold(gray, 91, 255, cv2.THRESH_BINARY)

    # This keeps the 'veins' ONLY where 'finger_mask' is White.
    clean_veins = cv2.bitwise_and(veins, veins, mask=finger_mask)

    # This removes small white dots (noise)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    clean_veins = cv2.morphologyEx(clean_veins, cv2.MORPH_OPEN, kernel)

    cv2.imshow("vein image of ahmed sial", clean_veins)
    cv2.imshow("raw image of ahmed sial", gray)
    cv2.imshow("enhanced image of ahmed sial", enhanced)

    




# image processing and display logic here bruh 








    # Check if 'q' key was pressed to quit program
    key =  cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break # Exit while loop, ending video cpature 
cv2.destroyAllWindows()