import cv2
import numpy as np

# Video capture object
vid = cv2.VideoCapture(0)
vid.set(3,1280)
vid.set(3,450)

# Threshold values tuned according to the background and colour of drawing object chosen
# Here I have chosen a blue bottle cap and these values are taken from the internet but one can tune according to their background
lower_range = np.array([110, 110, 50])
upper_range = np.array([150,255,255])

# For reducing the noise, we create a kernel
kernel = np.ones((9,9),np.uint8)

# This threshold is used to filter noise, the contour area must be bigger than this to qualify as an actual contour.
noiseth = 200
x1 = 0
y1 = 0
canvas = None

while(True):

    # Capture the video frame by frame
    ret, frame = vid.read()

    # To flip the frame horizontally(This is to be done if ur webcam gives u inverted image)
    frame = cv2.flip(frame, 1)

    # Initialize the canvas as a black image of the same size as the frame.
    if canvas is None:
        canvas = np.zeros_like(frame)

    # RGB to HSV .
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Filter the image and get the binary mask
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Perform the morphological operations to get rid of the noise.
    # Erosion removes the white part while dilation expands it.
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find Contours in the frame.
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # To make sure there is a contour present and its size is bigger than noise threshold.
    if contours and cv2.contourArea(max(contours,key = cv2.contourArea)) > noiseth:

        # Selecting the biggest contour with respect to area
        c = max(contours, key=cv2.contourArea)

        # Getting bounding box coordinates around that contour
        x, y, w, h = cv2.boundingRect(c)

        # Draw that bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # If there were no previous points then save the detected x2,y2
        # coordinates as x1,y1.
        # This is true when we writing for the first time or when writing
        # again when the pen had disappeared from view.
        if x1 == 0 and y1 == 0:
            x1, y1 = x, y
        else:
            # Draw the line on the canvas
            # To draw from the centroid of the bounding box

            x = x + int(w / 2)
            y = y + int(h / 2)
            canvas = cv2.line(canvas, (x1, y1), (x, y), [255, 255, 255], 10)

        # After the line is drawn the new points become the previous points.
        x1, y1 = x, y

    else:

        # If there were no contours detected then make x1,y1 = 0
        x1, y1 = 0, 0

    # To make it look as if the drawing is in the real actual frame.
    frame = cv2.add(frame, canvas)

    # stack the canvas and the frame
    stacked = np.hstack((canvas, frame))

    # Show this stacked frame at 40% of the size.
    cv2.imshow('Frame', cv2.resize(stacked, None, fx=0.6, fy=0.6))

    key = cv2.waitKey(1)

    # To reset the canvas
    if key == ord('q'):
        canvas = np.zeros_like(frame)

    # To quit press ESC
    if key == 27:
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()