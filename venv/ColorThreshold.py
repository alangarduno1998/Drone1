import cv2
import numpy as np
# cap = cv2.VideoCapture(0)
hsvVals_red = ([0, 154, 100], [20, 255, 255])
hsvVals_blue = ([50, 64, 42], [108, 255, 245])
hsvVals_yellow = ([23, 39, 123], [29, 255, 255])
hsvVals_orange = ([5, 125, 43], [9, 255, 255])
boundaries = [hsvVals_red, hsvVals_blue, hsvVals_yellow, hsvVals_orange]
threshold = 0.2
width, height = 480, 360
def multipleContours(img, ColorListC, ColorListA):
    i = 0
    for (lower, upper) in boundaries:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        biggest = max(contours, key=cv2.contourArea, default=0)
        try:
            x, y, w, h = cv2.boundingRect(biggest)
            cx, cy, area = x + w // 2, y + h // 2, w * h
            if area > 4000:
                cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                ColorListC.append((cx, cy)), ColorListA.append(area)
                i += 1
        except:
            print(f"null: {biggest} thrown at {i} iteration of finding color contour")
    print(len(ColorListA))
    if len(ColorListA) != 0:
        i = ColorListA.index(max(ColorListA))
        return img, [ColorListC, ColorListA]
    else:
        return img, [[0, 0], 0]

def thresholding(img):
    (lower, upper) = hsvVals_red
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    return mask
def getContours(imgThres, img, ColorListC, ColorListA):
    contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(biggest)
    cx, cy, area = x + w // 2, y + h // 2, w * h
    ColorListC.append((cx, cy)), ColorListA.append(area)
    cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    return ColorListC, ColorListA

while True:
    img = cv2.imread(r"C:\Users\alang\PycharmProjects\Drone1\venv\Resources\Images\1612900652.6954453.jpg")
    img = cv2.resize(img, (width, height))
    ColorListA, ColorListC, info = [], [], [[0, 0], 0]
    img, info = multipleContours(img, ColorListC, ColorListA)
    print(info)
    cv2.imshow("Output", img)
    # imgThres = thresholding(img)
    # ColorListC, ColorListA = getContours(imgThres, img, ColorListC, ColorListA)  # for translation
    # print(ColorListC, ColorListA)
    # cv2.imshow("Output", img)
    # cv2.imshow("Path", imgThres)
    cv2.waitKey(1)