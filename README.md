# Drone1
This repository allows you to navigate the DJI Ryze Tello using different methods ( Development in progress).

### Current Supported Vehicles
+ DJI Ryze Tello

### Current Features
- Drone Capture & Control using KeyBoard
- Color Tracking
- Aruco Marker Tracking
- Face Tracking

### Requirements
+ Python 3
+ OpenCV (MAIN) `pip3 install opencv-python`
+ OpenCV (CONTRIB) `pip3 install opencv-contrib-python`
+ DJITelloPY `pip3 install djitellopy`
+ keyboard `pip3 install keyboard`
+ NumPy `pip3 install numpy`

## Disclaimer
### Use the driver at your own risk, the creators of this code are NOT responsible in any way in case of accidents or damage, against users and/or objects.


Thank you for checking out my repository, if you use any of this please cite me.
-- Alan Garduno
## Drone Capture & Control using KeyBoard
### Installation
`pip3 install numpy opencv-python opencv-contrib-python djitellopy keyboard`

#### Turn on DJI Ryze Tello and connect to its WiFi
####To run script use:

`python venv\Drone Capture and Control.py`

### Control:
+ 't' - takeoff
+ 'l' - land
+ 'LEFT' - move left
+ 'RIGHT' - move right
+ 'UP' - move forward
+ 'DOWN' - move back
+ 'w' - move up
+ 's' - move down
+ 'a' - rotate counter clock-wise
+ 'd' - rotate clock-wise
,
### Capture:
+ 'z' - take picture and save to file location

#### Taking picture saves into file venv\Resources\Images

![DroneCapture](https://github.com/alangarduno1998/Drone1/blob/master/readmeImages/DroneCapture.png "Drone Capture")

+ Picture is taken during Drone Capture and Control to do some color thresholding on the four balloons

## Color Tracking
For this feature you will need to use the Color Picker and Color Threshold scripts

### Color Picker
Use Color Picker to determine the HSV minimum and maximum values of the color of the object you wish to track.
#### To run script use:
`python venv\ColorPicker.py`
#### Using picture saved from the Drone Capture & Control using KeyBoard section in file venv\Resources\Images or using your own image, slide the trackbar to extract the color feature of the object you wish to track.
![ColorPicker](https://github.com/alangarduno1998/Drone1/blob/master/readmeImages/ColorPicker.png "Color Picker")

+ Color Picking Stack(left) - original image included from file
+ Color Picking Stack(middle) - binary mask of image from using the HSV Trackbar
+ Color Picking Stack(right) - output image after applying mask from using the HSV Trackbar
+ HSV Trackbar - hue min/max, saturation min/max, vibrance min/max

#### Below is an example of a red balloon thresholded where teh hsv lower and upper values are printed in the terminal output
![Pick_Red](https://github.com/alangarduno1998/Drone1/blob/master/readmeImages/Pick_Red.png "Pick_Red")

+ HSV Trackbar - ([0, 187, 0], [4, 255, 255])

### Color Threshold
Use Color Threshold to determine the contours of the HSV values of the object you wish to track.
#### To run script use:
`python venv\ColorThreshold.py`
#### Using hsv values from the ColorPicker section, set a variable that contains the tuple of the hsv values and include it in the boundaries list.
![ColorThreshold](https://github.com/alangarduno1998/Drone1/blob/master/readmeImages/ColorThreshold.png "Color Threshold")

#### Total contours taken:
+ (topleft) hsvVals_red = ([0, 187, 0], [4, 255, 255])
+ (topright) hsvVals_blue = ([50, 64, 42], [108, 255, 245])
+ (bottomleft) hsvVals_yellow = ([23, 39, 123], [29, 255, 255])
+ (bottom right) hsvVals_orange = ([5, 125, 43], [9, 255, 255])

## Face Tracking
For this feature you will need to use the ObjectTracking script

#### Turn on DJI Ryze Tello and connect to its WiFi
Use ObjectTracking to follow your face with the haarcascade classifier (venv/Resources/haarcascade.xml).
#### To run script use:
`python venv\ObjectTracking.py`

## Aruco Marker Tracking
For this feature you will need to use the Aruco Tracking script

#### Turn on DJI Ryze Tello and connect to its WiFi
Use Aruco Tracking to follow the Aruco marker ( id = 0) using the ArUco libraries from tag system 4x4_50.
#### To run script use:
`python venv\ArucoTracking.py`