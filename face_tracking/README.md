# 🧍‍♂️ Face Direction Tracking – MobiCare

This module provides face direction-based control for the **MobiCare Smart Wheelchair**. Using **MediaPipe Face Mesh** and **OpenCV**, it detects whether a user is looking **left**, **right**, **forward**, **up**, or **down** — and optionally sends movement commands via **UART** to an STM32 microcontroller.

---

## 🧠 Overview

By tracking facial landmarks such as the **nose** and **eyes**, the system calculates relative positions and determines the head’s direction in real time.

This module can be used:
- As a standalone facial direction detector for testing and development.
- As part of the fully integrated AI control system that combines voice and face-based control.

---

## 🔍 Landmark Indices Used (MediaPipe)

| Feature     | Landmark Index |
|------------|----------------|
| Nose Tip    | `5`            |
| Left Eye    | `33`           |
| Right Eye   | `263`          |

---

## 🔄 Direction Detection Logic

- Nose centered between both eyes → **stop**
- Nose closer to left eye → **right**
- Nose closer to right eye → **left**
- Nose above eye level → **up**
- Nose significantly below → **down**

---

## 🆚 Comparison: Simple vs Integrated Script

| Feature | `face_direction_tracker.py` (Basic) | `run_face_detection_stream()` in AI System (Integrated) |
|--------|--------------------------------------|----------------------------------------------------------|
| Use Case | For simple testing and visualization | For full deployment on Raspberry Pi with UART & STM32 |
| Direction Output | Shown on-screen only (`cv2.imshow`) | Sent via UART + displayed on screen |
| Modes | Face direction only | Switchable via UART (voice / face) |
| UART Communication | ❌ Not included by default | ✅ Integrated |
| Interrupt Handling | ❌ Manual (ESC to exit) | ✅ STM32-controlled via UART |
| Integration with Voice Control | ❌ Separate script | ✅ Combined with `run_voice_detection()` |
| Suitable For | Developers testing face tracking logic | Final Raspberry Pi deployment system |

> ⚠️ If you're just testing face direction detection or debugging camera input, use the **basic version**.  
> For full AI integration, use the **combined script** with UART control.

---

## 📸 How It Works

1. Accesses the Raspberry Pi or USB camera.
2. Detects facial landmarks using MediaPipe.
3. Computes nose and eye positions.
4. Calculates movement direction.
5. Displays the direction on-screen (and optionally sends it to STM32 via UART).

---

## 💻 How to Run (Standalone)

### 1. Install Dependencies
```bash
pip install opencv-python mediapipe numpy

