import cv2
import numpy as np

# Callback Function
def nothing(x):
    pass

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(3,1280)
vid.set(3,450)


cv2.namedWindow('Trackbars')
cv2.resizeWindow('Trackbars',300,300)

# Creating trackbars with high and low values of Hue, Saturation and Value

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("U - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 0, 255, nothing)

# Initially we define the array as complete range

lower_range = np.array([0, 0, 0])
upper_range = np.array([179,255,255])

while (True):

    # Capture the video frame by frame
    ret, frame = vid.read()

    # To flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # RGB to HSV.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the new values of the trackbar in real time as the user changes them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Set the lower and upper HSV range according to the value selected by the trackbar
    # Press `s` to set the current values
    key = cv2.waitKey(1)
    if key == ord('s'):
        lower_range = np.array([l_h, l_s, l_v])
        upper_range = np.array([u_h, u_s, u_v])
        print("Lower range",lower_range)
        print("Upper range",upper_range)

    # Filter the image and get the binary mask, where white represents your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Converting the binary mask to 3 channel image, this is just so we can stack it with the others
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stack the mask, orginal frame and the filtered result
    stacked = np.hstack((mask_3, frame, res))

    # Show this stacked frame at 60% of the size.
    cv2.imshow('Frame', cv2.resize(stacked, None, fx=0.6, fy=0.6))

    # Press ESC to exit
    if key == 27:
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()