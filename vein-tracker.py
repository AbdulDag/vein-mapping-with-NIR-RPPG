import cv2 #OpenCV for video capture and display
import os







dataset_path = r"C:\Users\dagab\Desktop\vein-mapper\Finger Vein Database\002\left"  # Path to the dataset directory

try:
    file_list = os.listdir(dataset_path)
    images = [f for f in file_list if f.endswith(('.bmp', '.png', '.jpg'))]
    print(f"Found {len(images)} images in the dataset.")
    print("First image name:", images[0])
except FileNotFoundError:
    print("Error: The folder path is wrong. Check the path in 'dataset_path'")

#open cv stuff - Initializ webcam capture 
cap = cv2.VideoCapture(0) 

# Getting dimensions of the video frames 
Frame_width = int(cap.get(3)) # Width of the frame 
Frame_height = int(cap.get(4)) # Height of the frame

# Main video processing loop 
while True: 
    ret, frame = cap.read() # Capturing frame by frame from webcam
    if not ret: # checking if the fram was successfully captureed
        print("Failed to grab frame")
        break # Exit loop if frame capture fails 
    cv2.imshow("Webcam", frame) # Displays the current frame on a window 




# image processing and display logic here bruh 





    # Check if 'q' key was pressed to quit program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break # Exit while loop, ending video cpature 
cap.release()
cv2.destroyAllWindows()    # Convert the frame to grayscale
cv2.destroyAllWindows()