from djitellopy import tello
import numpy as np
import cv2
import time
import cv2.aruco as aruco
import os


w,h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

def initializeDrone():
    drone = tello.Tello()
    drone.connect()
    print(drone.get_battery())
    drone.streamon()
    drone.takeoff()
    time.sleep(1)
    drone.send_rc_control(0,0,0,0)
    time.sleep(2.2)
    return

def loadArucoImages(path):
    ObjectList = os.listdir(path)
    numOfMarkers = len(ObjectList)
    print("Total Number of Objects:", numOfMarkers)
    objDicts = {}
    for imgPath in ObjectList:
        key = int(os.path.splitext(imgPath)[0])
        frameEmbed = cv2.imread(f'{path}/{imgPath}')
        objDicts[key] = frameEmbed
    return objDicts

def FindArucoMarkers(frame, markerSize = 6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #key = getattr(aruco, f'DICT_{markersize}X{markerSize}_{totalMarkers}')
    key = getattr(aruco, f'DICT_ARUCO_ORIGINAL')
    aruco_dict = aruco.Dictionary_get(key)
    arucoParameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters = arucoParameters)
    #print(ids)
    if draw:
        display = aruco.drawDetectedMarkers(frame, corners, ids)
    return [corners, ids]

def FindFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade.xml ")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,8)

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y +h), (0, 0, 255), 2)
        cx = x + w//2
        cy = y + h//2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255,0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]



def FaceTrack(drone, info, w, pid, perror):
    area = info[1]
    x,y = info[0]
    fb = 0

    error = x - w//2
    speed = pid[0]*error +pid[1]*(error-perror)
    speed = int(np.clip(speed,-100,100))
    area = info[1]
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area> fbRange[1]:
        fb=-20
    elif area < fbRange[0] and area !=0:
        fb=20

    print(speed, fb)

    if x == 0:
        speed = 0
        error = 0
    drone.send_rc_control(0, fb, 0, speed)
    return error
def main():
    initializeDrone()
    cap = cv2.VideoCapture(0)
    objDicts = loadArucoImages("Objects")

    while True:
        #_, img = cap.read()
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (w, h))
        img, info = FindFace(img)
        pError = FaceTrack(drone, info, w, pid, pError)
        print("Center", info[0], "Area", info[1])
        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land
            break
if __name__ == "__main__":
    main()