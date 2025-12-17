import cv2 #OpenCV for video capture and display
import os
import numpy as np





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
    if frame is None: 
        print(f"Error loading image: {full_path}")
        continue # Skips to next image in the loop 
    height, width = frame.shape[:2]
    frame = frame[60:height-60, :]
    # Checking if image failed to load
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the image to greyscale
    
    # -- Enhance image contrast --
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) # Creating a clahen (Contrast limited adaptive histogram equalization) object 
    enhanced = clahe.apply(gray)

    #now we add adaptive thresholding
    #we make the veins pure white and then use gaussian blur to smooth the image

    #change block size and c value respectively to adjust vein visibility. block size is basically for the noise and if vein broken or invisible lower c value. if too much noise increase block size
    veins = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 5)



    # add masking cuz its detecting outside the finger area too
    #tweak second parameter if it cust off too mcuh of finger or includes too much background
    _, binary_mask = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    #find all shapes in the image
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(gray)
    # Checking if countor were found
    if contours:
        largest_contour = max(contours, key=cv2.contourArea) # finds largest contour and sorts by their area
        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED) # Draws largest contour on mask as a filled white shape
        mask = cv2.erode(mask, np.ones((5,5), np.uint8), iterations=3) # Removes noisy egde articats 
    # This keeps the 'veins' ONLY where 'finger_mask' is White.
    clean_veins = cv2.bitwise_and(veins, veins, mask=mask)

    # This removes small white dots (noise)
    closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,8))
    clean_veins = cv2.morphologyEx(clean_veins, cv2.MORPH_CLOSE, closing_kernel)

    # ... Now start the SKELETONIZATION loop ...
    skeleton = np.zeros(clean_veins.shape, np.uint8)
    
    # 2. Get a structural element (a cross shape works best for lines)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    
    # 3. Loop until no white pixels are left in the temp image
    temp_img = clean_veins.copy()
    while True:
        # Erode (shrink) the white lines
        eroded = cv2.erode(temp_img, element)
        
        # Dilate (grow) them back to see what we lost
        temp = cv2.dilate(eroded, element)
        
        # Subtract to find the "edges" that were removed
        temp = cv2.subtract(temp_img, temp)
        
        # Add those edges to our permanent skeleton
        skeleton = cv2.bitwise_or(skeleton, temp)
        
        # Update for next loop
        temp_img = eroded.copy()
        
        # Stop if the image is completely black
        if cv2.countNonZero(temp_img) == 0:
            break

    # Show the final result
    cv2.imshow("Skeleton (Final Map)", skeleton)
    
    # ... then your other imshow lines ...
    cv2.imshow("vein image of ahmed sial", clean_veins)
    cv2.imshow("raw image of ahmed sial", gray)
    cv2.imshow("enhanced image of ahmed sial", enhanced)

    




# image processing and display logic here bruh 








    # Check if 'q' key was pressed to quit program
    key =  cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break # Exit while loop, ending video cpature 
cv2.destroyAllWindows()