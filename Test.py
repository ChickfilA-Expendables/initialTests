import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

img = cv2.imread('../trainingData/frames/frame0.jpg')
#img = cv2.imread('image.jpg')
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


#print res.shape
plt.figure(1)
plt.imshow(res)
#plt.show()
x = res.shape[0]
y = res.shape[1]

t = range(0,x)
y_red = []
y_blue = []
y_green = []
avg = []
sample_r = res[300][400] #res[x/2][y/2]
print sample_r
for i in range(x):
  avg.append(int(res[i][400][0]*float(sample_r[0])/float(255) + res[i][400][1]*float(sample_r[1])/float(255) + res[i][400][2]*float(sample_r[2])/float(255)))
  y_red.append(res[i][400][0])
  y_green.append(res[i][400][1])
  y_blue.append(res[i][400][2])

#for i in range(x):
  #print (y_red[i] * sample_r[0]/255) #+ y_green[i] * sample_r[1]/255 + y_blue[i] * sample_r[2]/255)

container = 0.0
break_condition = 0
for i in avg:
  if (i != 0):
    container = container + 1
  else:
    break_condition = break_condition + 1
  if (break_condition > 5):
    break
maxValue = 0.0
for i in t:
  if (avg[i] > maxValue):
    maxValue = i
percant = maxValue / container * 100
#percant = 100 - percant
if (percant > 100):
  percant = 0

print "lemonade level = ",percant
print "container length = ",container

#plt.figure(2)
#plt.plot(t,y_red)
#plt.figure(3)
#plt.plot(t,y_green)
#plt.figure(4)
#plt.plot(t,y_blue)
plt.figure(2)
plt.plot(t,avg)
plt.show()

#canny = cv2.Canny(res, 100, 200)
#cv2.imwrite("canny.bmp", canny)
