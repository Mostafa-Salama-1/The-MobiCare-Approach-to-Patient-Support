# 👁️ Eye Tracking – MobiCare

This module implements **eye gaze direction detection** using **MediaPipe Face Mesh** and **OpenCV** to control the **MobiCare Smart Wheelchair**. It analyzes the user’s eye movement and determines their intended direction (e.g., **Forward**, **Left**, **Right**, **Up**, or **Down**) without any physical movement.

---

## 🧠 Overview

The system detects specific eye landmarks from the user's **left eye**, isolates the eye region, and uses image processing techniques to locate the **iris position**. Based on this position, it classifies the user's gaze direction in real time and displays it on the screen.

This direction can later be mapped to wheelchair control commands or sent via UART to a microcontroller.

---

## 🔍 Landmarks Used (MediaPipe Face Mesh)

| Feature        | Landmark Index |
|----------------|----------------|
| Left Eye – Left Corner   | `285` |
| Left Eye – Right Corner  | `276` |
| Left Eye – Bottom Center | `450` |

---

## 🎯 Gaze Direction Logic

The script calculates the iris center `(x, y)` and compares it with screen regions:

| Iris Position   | Detected Direction |
|------------------|--------------------|
| Center           | `Forward`          |
| Far Left         | `Left`             |
| Far Right        | `Right`            |
| Top Center       | `Up`               |
| Bottom Center    | `Down`             |
| Diagonals        | `Up-Left`, `Down-Right`, etc. |

---

## 🛠️ How It Works

1. Captures live video stream from a webcam or Raspberry Pi camera.
2. Uses **MediaPipe** to detect facial landmarks.
3. Extracts a small bounding box around the left eye using landmark coordinates.
4. Applies grayscale, blur, and thresholding to detect contours.
5. Finds the largest contour assumed to be the **iris**.
6. Calculates the center of the iris and compares it with predefined screen regions.
7. Displays the detected direction on the screen and optionally sends it as a command.

---

## 📦 Files Included

| File | Description |
|------|-------------|
| `eye_tracking.py` | Main script for eye direction detection |
| `README.md`       | This file |

---

## 💻 How to Run

### 1. Install Dependencies
```bash
pip install opencv-python mediapipe numpy

