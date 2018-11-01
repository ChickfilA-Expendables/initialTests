import cv2.cv as cv
import cv2
import numpy as np

orig = cv.LoadImage('../trainingData/frames/frame0.jpg', cv.CV_LOAD_IMAGE_COLOR)
im = cv.CreateImage(cv.GetSize(orig), 8, 1)
cv.CvtColor(orig, im, cv.CV_BGR2GRAY)
#Keep the original in colour to draw contours in the end

cv.Threshold(im, im, 128, 255, cv.CV_THRESH_BINARY)
#cv.ShowImage("Threshold 1", im)

element = cv.CreateStructuringElementEx(5*2+1, 5*2+1, 5, 5, cv.CV_SHAPE_RECT)

cv.MorphologyEx(im, im, None, element, cv.CV_MOP_OPEN) #Open and close to make appear contours
cv.MorphologyEx(im, im, None, element, cv.CV_MOP_CLOSE)
cv.Threshold(im, im, 128, 255, cv.CV_THRESH_BINARY_INV)
cv.ShowImage("After MorphologyEx", im)
cv.ShowImage("Original", orig)
# --------------------------------

#origArray = np.asarray(orig)
#mask = np.asarray(im)
mask = cv2.imread(im)
cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
out = 0
#cv2.bitwise_and(origArray, out, mask=mask)
#cv.ShowImage("After Mask", res)

vals = cv.CloneImage(im) #Make a clone because FindContours can modify the image
contours=cv.FindContours(vals, cv.CreateMemStorage(0), cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0,0))

_red = (0, 0, 255); #Red for external contours
_green = (0, 255, 0);# Gren internal contours
levels=1 #1 contours drawn, 2 internal contours as well, 3 ...
cv.DrawContours (orig, contours, _red, _green, levels, 2, cv.CV_FILLED) #Draw contours on the colour image

#cv.ShowImage("Image", orig)
cv.WaitKey(0)
