import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
img = cv2.imread('../trainingData/frames/frame0.jpg')

# Prepocess
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
flag, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

# Find contours
img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True) 

# Select long perimeters only
perimeters = [cv2.arcLength(contours[i],True) for i in range(len(contours))]
listindex=[i for i in range(15) if perimeters[i]>perimeters[0]/2]
numcards=len(listindex)

card_number = -1 #just so happened that this is the worst case
stencil = np.zeros(img.shape).astype(img.dtype)
cv2.drawContours(stencil, [contours[listindex[card_number]]], 0, (255, 255, 255), cv2.FILLED)
res = cv2.bitwise_and(img, stencil)
cv2.imwrite("out.bmp", res)

t = range(0,720)
y_red = []
y_blue = []
y_green = []

#print res.shape
plt.figure(1)
#plt.subplot(141)
plt.imshow(res)

for i in range(res.shape[0]):
  avg = (res[i][400][0] + res[i][400][1] + res[i][400][2])/3
  y_red.append(res[i][400][0])
  y_green.append(res[i][400][1])
  y_blue.append(res[i][400][2])
#plt.subplot(142)
plt.figure(2)
plt.plot(t,y_red)
#plt.subplot(143)
plt.figure(3)
plt.plot(t,y_green)
#plt.subplot(144)
plt.figure(4)
plt.plot(t,y_blue)
plt.show()
#canny = cv2.Canny(res, 100, 200)
#cv2.imwrite("canny.bmp", canny)
