# SoundFlux

SoundFlux is a Python-based hand-tracking project that allows you to control your Mac's system volume using hand gestures. 

It uses your computer's webcam to detect your hand and calculates the distance between your thumb and index finger to seamlessly adjust the volume.

## Built With

- **Python**
- **OpenCV** (`cv2`) - For webcam capturing and drawing.
- **MediaPipe** - For hand and finger landmark detection.
- **AppleScript** (`osascript`) - Used to programmatically adjust the macOS system volume.

## Files
- `HandTrackingModule.py`: Contains the core hand detection logic using MediaPipe.
- `VolumeHandControl.py`: Contains the main loop that captures the camera feed, calculates finger distance, and changes your system volume accordingly.
- `HandTrackingMin.py` / `MyNewGameHandTracking.py`: Additional examples for hand-tracking detection.

## Requirements
To install the required packages:
```bash
pip install opencv-python mediapipe numpy sounddevice
```

## How to use

Run the volume control script:
```bash
python VolumeHandControl.py
```

Once tracking starts, place your hand in front of the camera:
- **Thumb and Index Finger:** The distance between the tip of your thumb and the tip of your index finger determines the volume.
- Move them closer to lower the volume, or further apart to increase it.
- Press `q` to quit the application.

## Note
This project specifically uses macOS `osascript` commands to control the volume. If you are trying to run this on Windows or Linux, you will need to replace the `osascript` command on line 49 of `VolumeHandControl.py` with an equivalent audio control library for your OS.
