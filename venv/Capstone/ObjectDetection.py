import numpy as np
import cv2
import cv2.aruco as aruco
import os

camera_matrix = np.float32([[1448, 0, 624], [0, 1448, 316], [0, 0, 1]])
dist_coeff = np.float32([0.05437520427175414, 0.010684173729094198, 0.003107828628462368, -0.00950183296786585, 4.68352656147056])

def loadarucoimages(path):
    objectlist = os.listdir(path)
    numofmarkers = len(objectlist)
    #print("Total Number of Objects:", numofmarkers)
    objdicts = {}
    for imgpath in objectlist:
        key = int(os.path.splitext(imgpath)[0])
        frameembed = cv2.imread(f'{path}/{imgpath}')
        objdicts[key] = frameembed
    return objdicts


def findarucomarkers(frame, markersize = 6, totalmarkers=250, draw=True):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # key = getattr(aruco, f'DICT_{markersize}X{markersize}_{totalmarkers}')
    key = getattr(aruco, f'DICT_APRILTAG_36H11')
    aruco_dict = aruco.Dictionary_get(key)
    arucoparameters = aruco.DetectorParameters_create()
    corners, ids, rejectedimgpoints = aruco.detectMarkers(gray, aruco_dict, parameters = arucoparameters, cameraMatrix=camera_matrix, distCoeff=dist_coeff)
    # print(ids)
    if draw:
        display = aruco.drawDetectedMarkers(frame, corners, ids)
    return [corners, ids]


def findaruco(corners, id, frame, frameembed, ArucoListC, ArucoListArea, drawPose=True, drawIm=True):
    cx = (corners[0][0][0] +corners[0][2][0]) / 2
    cy = (corners[0][0][1] + corners[0][3][1]) / 2
    rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners, 0.02, camera_matrix,
                                                               dist_coeff)
    (rvec - tvec).any()  # get rid of that nasty numpy value array error
    ArucoListC.append([cx, cy])
    area = cv2.contourArea(corners)
    ArucoListArea.append(area)
    if drawPose:
        aruco.drawAxis(frame, camera_matrix, dist_coeff, rvec, tvec, 0.0375)
        # testing this
        cv2.putText(frame, str(int(area)), (int(cx), int(cy)), cv2.FONT_ITALIC, 0.7, (0, 255, 0), 1)
        cv2.putText(frame, str(int(cx)) +str(",") + str(int(cy)), (int(cx), int(corners[0][0][1])), cv2.FONT_ITALIC, 0.7, (0, 255, 0), 1)

    frameout = frame
    if drawIm:
        p1 = (corners[0][0][0], corners[0][0][1])  # top left corner (x,y)
        p2 = (corners[0][1][0], corners[0][1][1])  # top right corner (x,y)
        p3 = (corners[0][2][0], corners[0][2][1])  # bottom left corner (x,y)
        p4 = (corners[0][3][0], corners[0][3][1])  # bottom right corner (x,y)
        pts_dst = np.array([p1, p2, p3, p4])
        size = frameembed.shape  # height ,width ,center
        pts_src = np.array(
            [
                [0, 0],
                [size[1] - 1, 0],
                [size[1] - 1, size[0] - 1],
                [0, size[0] - 1]
            ], dtype=float
        )
        matrix, status = cv2.findHomography(pts_src, pts_dst)
        frameout = cv2.warpPerspective(frameembed, matrix, (frame.shape[1], frame.shape[0]))
        cv2.fillConvexPoly(frame, pts_dst.astype(int), 0, 16)
        frameout = frame + frameout
    return frameout, ArucoListC, ArucoListArea


def main():
    cap = cv2.VideoCapture(0)
    objdicts = loadarucoimages("Objects")
    while True:
        ret, frame = cap.read()
        loadarucoimages("Objects")
        ArucoListArea = []
        ArucoListC = []
        info = [[0, 0], [0]]
        arucofound = findarucomarkers(frame)
        if len(arucofound[0]) != 0:
            for corners, id in zip(arucofound[0], arucofound[1]):
                if int(id) in objdicts.keys():
                    frame, info[0], info[1] = findaruco(corners, id, frame, objdicts[int(id)], ArucoListC, ArucoListArea, drawPose=True, drawIm=False)
        if len(info[1]) == 1:
            print(info[0],info[1])
        cv2.imshow('Display', frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()