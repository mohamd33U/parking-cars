import cv2
import pickle
import numpy as np

# Dimensions of each parking space (width and height)
w, h = 107, 48

# Load the video file
cap = cv2.VideoCapture('checkn.mp4')

# Load the parking position coordinates
with open('parkingpos', 'rb') as f:
    poslist = pickle.load(f)


# Function to check the parking space status
def checkparkingspace(img, output_img):
    for pos in poslist:
        x, y = pos
        imgcrop = img[y:y + h, x:x + w]
        count = cv2.countNonZero(imgcrop)

        # Print the count value for debugging
        print(f"Position {pos}: Non-zero count = {count}")

        # Determine the color based on the non-zero pixel count
        if count < 800:
            color = (0, 255, 0)  # Green for unoccupied
            status = "Free"
        else:
            color = (0, 0, 255)  # Red for occupied
            status = "Occupied"

        # Draw rectangle around the parking space
        cv2.rectangle(output_img, pos, (pos[0] + w, pos[1] + h), color, 2)
        # Put the count value and status text on the rectangle
        cv2.putText(output_img, str(count), (x, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(output_img, status, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


# Loop to process the video frame by frame
while True:
    ret, img = cap.read()
    if not ret:
        break

    # Convert to grayscale
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    imgblur = cv2.GaussianBlur(imggray, (3, 3), 1)
    # Apply adaptive threshold
    imgtresh = cv2.adaptiveThreshold(imgblur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 16)
    # Apply median blur
    imgmed = cv2.medianBlur(imgtresh, 5)
    # Apply dilation
    kern = np.ones((3, 3), np.uint8)
    fin = cv2.dilate(imgmed, kern, iterations=1)

    # Create a copy of the original image to draw rectangles
    output_img = img.copy()

    # Check parking spaces
    checkparkingspace(fin, output_img)

    # Display the frame with parking space status
    cv2.imshow("Parking Status", output_img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
