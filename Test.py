import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import picamera
import requests as req
import sys

lemonadeURL = 'https://young-anchorage-97125.herokuapp.com/data/1.json'
ketchupURL = 'https://young-anchorage-97125.herokuapp.com/data/3.json'

def expendableData(expendable, value):
    if expendable == 'lemonade':
        print('Sending Lemonade Data to Server...')
        url = lemonadeURL
    elif expendable == 'ketchup':
        print('Sending Ketchup Data to Server...')
        url = ketchupURL
    else:
        print('Not a Valid Expendable')
        return None
    payload = {'value' : value}
    r = req.patch(url, payload)
    if r.status_code >= 200 and r.status_code < 300:
        print('Successfully updated')
    else:
        print('Status Code:' + r.status_code)


def contours(img):
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
  return res

def calculateLevel(res):
  x = res.shape[0]
  y = res.shape[1]

  t = range(0,x)
  y_red = []
  y_blue = []
  y_green = []
  avg = []
  diff = []
  sample_r = res[x/2][y/2]
  level_r = 0
  level_g = 0
  level_b = 0
  level_diff = 0
  thresh = 3
  for i in range(x):
    diff.append(abs((int(sample_r[0]) - int(res[i][y/2][0])) + (int(sample_r[1]) - int(res[i][y/2][1])) + (int(sample_r[2]) - int(res[i][y/2][2]))))
    #y_red.append(abs(int(sample_r[0]) - int(res[i][y/2][0])))
    #y_green.append(abs(int(sample_r[1]) - int(res[i][y/2][1])))
    #y_blue.append(abs(int(sample_r[2]) - int(res[i][y/2][2])))
    red = abs(int(sample_r[0]) - int(res[i][y/2][0]))
    green = abs(int(sample_r[1]) - int(res[i][y/2][1]))
    blue = abs(int(sample_r[2]) - int(res[i][y/2][2]))
    difference = abs((int(sample_r[0]) - int(res[i][y/2][0])) + (int(sample_r[1]) - int(res[i][y/2][1])) + (int(sample_r[2]) - int(res[i][y/2][2])))
    if (difference < 15):
      level_diff+= 1
    if (red < 9):
      level_r += 1
    if (green < 7):
      level_g += 1
    if (blue < 5):
      level_b += 1
    #avg.append(int(res[i][y/2][0]*(1-float(sample_r[0])/float(255)) + res[i][y/2][1]*(1-float(sample_r[1])/float(255)) + res[i][y/2][2]*(1-float(sample_r[2])/float(255))))
    y_red.append(res[i][y/2][0])
    y_green.append(res[i][y/2][1])
    y_blue.append(res[i][y/2][2])
    #res[i][y/2] = [255,0,0]
  container = 0.0
  break_condition = 0
  for i in y_red:
    if (i != 0):
      container = container + 1
    else:
      break_condition = break_condition + 1
    if (break_condition > 5):
      break
  percant = level_diff / container * 100
  return [level_r, level_g, level_b, level_diff, percant]


img = cv2.imread('pictures/image4.jpg')
out = contours(img)
calc = calculateLevel(out)
print calc

#camera = picamera.PiCamera()
#camera.capture('image.jpg')
#img = cv2.imread('../trainingData/frames/frame0.jpg')

#plt.figure(1)
#plt.imshow(res)
#fig,ax = plt.subplots(1,1)
#ax.imshow(res)
#fig.canvas.draw()
#plt.show()

#maxValue = 0.0
#for i in t:
#  if (avg[i] > maxValue):
#    maxValue = i
#print maxValue
#percant = 100 - percant
#if (percant > 100):
#  percant = 0

#print "lemonade level = ",percant
#print sample_r
#print "container length = ",container
#print "level_r = ",level_r
#print "level_g = ",level_g
#print "level_b = ",level_b
#print "level_diff = ",level_diff
#print "percant = ",percant
#plt.figure(2)
#plt.plot(t,diff)
#plt.figure(3)
#plt.plot(t,y_green)
#plt.figure(4)
#plt.plot(t,y_blue)
#plt.figure(5)
#plt.plot(t,y_red)
#plt.show()
#expendableData('lemonade', 65)
#canny = cv2.Canny(res, 100, 200)
#cv2.imwrite("canny.bmp", canny)
