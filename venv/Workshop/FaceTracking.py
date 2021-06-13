from djitellopy import tello
import numpy as np
import cv2, time

def initializeDrone():
    drone = tello.Tello()
    drone.connect()
    drone.land()
    time.sleep(2)
    print(drone.get_battery())
    drone.streamon()
    drone.takeoff()
    time.sleep(2)
    drone.send_rc_control(0,0,20,0)
    time.sleep(2.2)
    return drone
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
        cv2.circle(img, (int(cx), int(cy)), 5, (0, 255,0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]
def FaceTrack(drone, info, w,h, pid, perror, fbRange):
    area = info[1]
    x,y = info[0]
    fb = 0
    error = [x - w//2, h//2-y]
    speed = [pid[0]*error[0] +pid[1]*(error[0]-perror[0]), pid[3]*error[1] +pid[4]*(error[1]-perror[1])]
    speed[0] = int(np.clip(speed[0], -100, 100))
    speed[1] = int(np.clip(speed[1],-100,100))
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area> fbRange[1]:
        fb=-20
    elif area < fbRange[0] and area !=0:
        fb=20
    if x == 0:
        speed[0] = 0
        error[0] = 0
    if y == 0:
        speed[1] = 0
        error[1] = 0
    drone.send_rc_control(0, fb, speed[1], speed[0])
    return error

def main():
    drone = initializeDrone()
    w, h = 360, 240
    fbRange = [6200, 6800]
    abRange = [20000, 26000]
    pd = [0.6, 0.7, 0, 0.7,0.8,0]
    pError = [0,0]
    while True:
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (w, h))
        img, info = FindFace(img)
        pError = FaceTrack(drone, info, w,h, pd, pError, fbRange)
        cv2.imshow("Output", img)
        print("Center", info[0], "Area", info[1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land
            break
if __name__ == "__main__":
    main()