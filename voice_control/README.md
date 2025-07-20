# 🎤 Voice Control – MobiCare

This module contains the code and model used to recognize voice commands and control the smart wheelchair accordingly. The system uses a custom-trained deep learning model to classify spoken words like `"forward"`, `"backward"`, `"left"`, `"right"`, and `"stop"` and sends the corresponding movement commands to the STM32 microcontroller via UART.

---

## 🧠 Overview

The voice control system runs on the **Raspberry Pi 4** and uses a microphone to capture the user’s voice in real-time. The captured audio is processed and passed to a trained deep learning model. If a valid command is recognized with high confidence, a corresponding direction command is sent to the STM32 through UART.

---

## 🎯 Model Commands

- `forward`
- `backward`
- `left`
- `right`
- `stop`

---

## 🧪 Dataset

The model was trained using a combination of:
- **Google Speech Commands Dataset**
- **Custom recorded WAV files**
  
All audio files were 1-second `.wav` clips labeled accordingly.

---

## 🔄 Processing Pipeline

### 1. **Data Collection**
- Public + custom recorded voice samples
- 5 labels: forward, backward, left, right, stop

### 2. **Preprocessing (Librosa)**
- Pad/truncate to 1 second (8000 samples)
- Convert to 64-band mel-spectrogram (log-scaled)
- Data augmentation:
  - Add noise
  - Time shift
  - Pitch shift
  - Time stretch
  - Volume change

### 3. **Model Architecture**
- Input Layer (mel-spectrogram)
- 1D Convolutional layers
- Batch Normalization, Pooling, Dropout
- LSTM Layer
- Dense layers for classification

### 4. **Training**
- Loss: Categorical Crossentropy
- Optimizer: Adam
- Metric: Accuracy

---

## 💻 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
