import cv2
import numpy as np
cap = cv2.VideoCapture(0)
hsvVals_red = [0, 154, 100, 179, 255, 255]
threshold = 0.2
width, height = 480, 360

def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals_red[0], hsvVals_red[1], hsvVals_red[2]])
    upper = np.array([hsvVals_red[3], hsvVals_red[4], hsvVals_red[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def getContours(imgThres, img):
    contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(biggest)
    cx = x + w // 2
    cy = y + h // 2
    cv2.drawContours(img, biggest, -1, (255,0,255), 7)
    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

while True:
    img = cv2.imread(r"C:\Users\alang\PycharmProjects\Drone1\Resources\Images\1612900400.1704762.jpg")
    img = cv2.resize(img, (width, height))
    img = cv2.flip(img, 0)

    imgThres = thresholding(img)

    cx = getContours(imgThres, img)  # for translation
    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThres)
    cv2.waitKey(1)