# Virtual Drawing Pad using OpenCV

### This is a mini project to learn basic concepts of OpenCV

The project involves 2 parts 
1. Finding the correct range of HSV values according to the colour of the object to be used to draw and background.
2. Take the values and plug it in in the drawing code to use the virtual drawing pad

### Results
 
![](https://i.imgur.com/cl2a7j4.gif)
 
 ![](https://i.imgur.com/o5Po3Ka.gif)



### This project required basic understanding of the following concepts
- [x] Thresholding
- [x] RGB to HSV color spaces 
- [x] Morphological operations(Erode and Dilate)
- [x] Contours 
- [x] Bounding Box
- [x] Masking

### The following points should be noted:

- Thresholding is performed on HSV and not on RGB because HSV, it separates the image intensity, from the color information. 
- Morphological operations are used to remove any noise if present.
