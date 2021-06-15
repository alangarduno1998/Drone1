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
![Alt text](https://github.com/alangarduno1998/Drone1/tree/master/readmeImages/DroneCapture.png "Drone Capture")

+ Picture is taken during Drone Capture and Control to do some color thresholding on the four balloons

###