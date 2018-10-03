import picamera
import cv2
import numpy as np

videoDirectory = "../trainingData/CFA_LEMONADE_FOOTAGE.mp4"
saveDirectory = "../trainingData/frames"
vidcap = cv2.VideoCapture(videoDirectory)
success,image = vidcap.read()
count = 0;
while success:
  cv2.imwrite(saveDirectory + "/frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
