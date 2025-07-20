# 🦽 Smart Wheelchair – MobiCare

**MobiCare** is a smart wheelchair system developed as a graduation project by students at the Faculty of Engineering, Benha University (Communication and Computer Department). The project is designed to enhance mobility and independence for people with disabilities by integrating modern technologies like **Artificial Intelligence**, **Embedded Systems**, and **Mobile Applications**.

---

## 📌 Problem Statement

Many individuals with physical disabilities face difficulties using traditional wheelchairs, particularly when they are unable to operate them manually. Existing smart solutions are often expensive and lack features like intelligent control or real-time health monitoring.

**MobiCare** aims to solve these problems by offering a cost-effective and intelligent solution for:
- Smart and remote-controlled movement
- Multiple control modes
- Real-time health monitoring
- Increased user independence and safety

---

## 🎯 Project Objectives

- Enable multiple control modes:
  - Voice Commands
  - Face Direction Tracking
  - Eye Tracking
  - Mobile App
  - Joystick
- Provide real-time health monitoring
- Allow easy integration between AI systems and embedded devices
- Design a clean, accessible user interface for patient control and caregiver monitoring

---

## 🧠 System Overview

MobiCare consists of multiple components working together:

| Component        | Description |
|------------------|-------------|
| **STM32 MCU**     | Main controller managing movement and control modes |
| **Raspberry Pi 4** | Runs AI models for voice, face, and eye tracking |
| **ESP8266**       | Wi-Fi module connecting mobile app and Firebase |
| **Mobile App**    | Flutter-based UI for control and patient health management |
| **Health Sensors**| Heartbeat (MAX30102) and Temperature (MLX90614) sensors |
| **Camera**        | Used for face and eye tracking |
| **Joystick**      | Manual mode for traditional analog movement |

---

## 🔄 Control Modes Logic

The user selects the mode via push buttons connected to the STM32, which handles:

- Reading joystick values via ADC
- Receiving commands from:
  - Raspberry Pi (voice/face/eye)
  - Mobile App via ESP8266
- Sending signals to the BTS7960 motor driver for movement

---

## 🤖 AI Components

### 🎤 Voice Recognition
- Deep neural network trained on "forward", "backward", "left", "right", and "stop" commands
- Preprocessing includes noise addition, time shifting, pitch change, mel-spectrogram conversion
- Architecture: 1D CNN + LSTM

### 👁️ Eye Tracking
- Detects iris position using OpenCV
- Translates eye direction to control commands (Left, Right, Forward, Stop)

### 🧍‍♂️ Face Direction Tracking
- Uses MediaPipe Face Mesh
- Analyzes nose position relative to eyes to determine direction

---

## 📱 Mobile Application

- Built with **Flutter**
- Integrated with **Firebase** for:
  - Authentication
  - Real-time data storage (Cloud Firestore)
- Clean, modern UI (light & dark modes)
- Includes features:
  - Manual wheelchair control
  - Patient information, history, reminders, and medical records
  - Real-time temperature and heartbeat display
  - Google Drive upload for medical files

---


## 📊 Testing & Results

- Wheelchair successfully controlled via all modes
- Real-time command transmission verified through UART
- Health data stored and retrieved successfully using Firebase
- Smooth interaction between all subsystems

---

## 📁 Repository Structure

