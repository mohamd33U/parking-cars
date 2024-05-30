import cv2
import pickle

# Load the image
img = cv2.imread('carParkImg.png')

# Width and height of the parking space rectangles
w, h = 107, 48

# Try to load the parking positions from the pickle file, create an empty list if the file doesn't exist
try:
    with open('parkingpos', 'rb') as f:
        poslist = pickle.load(f)
except (FileNotFoundError, EOFError):
    poslist = []


def mouseclick(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Add a new parking position
        poslist.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        # Remove a parking position if the right mouse button is clicked inside a rectangle
        for i, pos in enumerate(poslist):
            x1, y1 = pos
            if x1 < x < x1 + w and y1 < y < y1 + h:
                poslist.pop(i)
                break


# Main loop
while True:
    # Display the image
    img_copy = img.copy()  # Make a copy of the image to draw the rectangles on
    for pos in poslist:
        cv2.rectangle(img_copy, pos, (pos[0] + w, pos[1] + h), (0, 255, 0), 2)
    cv2.imshow('img', img_copy)

    # Set the mouse callback function
    cv2.setMouseCallback('img', mouseclick)

    # Check for 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the parking positions to a pickle file when the program exits
with open('parkingpos', 'wb') as f:
    pickle.dump(poslist, f)

# Release resources and close windows
cv2.destroyAllWindows()
