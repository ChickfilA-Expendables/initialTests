import picamera
import cv2
import argparse
import imutils

camera = picamera.PiCamera()
camera.capture('image.jpg')

class ShapeDetector:
  def __init__(self):
    pass
  def detect(self, c):
    shape = "unidentified"
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c, .04*peri, True)
    if len(approx) == 3:
      shape = "triangle"
    elif len(approx) == 4:
      (x, y, w, h) = cv2.boundingRect(approx)
      ar = w / float(h)
      shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    elif len(approx) == 5:
      shape = "pentagon"
    else:
      shape = "circle"
    return shape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()
