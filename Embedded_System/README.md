# 🔧 Embedded System – MobiCare Smart Wheelchair

This directory contains the **STM32 (C-based)** firmware for the **MobiCare Smart Wheelchair**, responsible for receiving commands, reading joystick input, and controlling motor drivers based on various control modes.

---

## 🎯 Core Responsibilities

- 🕹️ **Joystick control** via ADC: manual driving mode using analog stick
- 🔁 Receive AI commands via **UART2 (voice)** and **UART3 (face/eye detection)**
- ⚙️ Control DC motors through GPIO outputs
- 🚦 Switch between multiple **modes** using input buttons

---

## 🧱 Hardware Architecture

| Component         | Description                            |
|------------------|----------------------------------------|
| **MCU**          | STM32F103 or similar                   |
| **Joystick**     | Analog stick for direct control        |
| **ADC1/ADC2**    | Reads X/Y values from joystick         |
| **UART2**        | Voice commands from Raspberry Pi       |
| **UART3**        | Eye/face control signals               |
| **GPIO Outputs** | Controls motor drivers (IN1–IN4)       |
| **GPIO Inputs**  | Buttons to change between control modes|

---

## 🎮 Joystick Control (Mode 1)

In **Mode 1**, the user can manually control the wheelchair using an **analog joystick** connected to **ADC1 and ADC2**. The direction is determined based on threshold comparisons of X and Y analog values:

| Axis        | Threshold         | Direction |
|-------------|-------------------|-----------|
| X < 1000    | Left              |
| X > 3000    | Right             |
| Y < 1000    | Forward (Up)      |
| Y > 3000    | Backward (Down)   |
| Else        | Stop              |

---

## 🚦 Control Modes

| Mode | Input Method | Description                              |
|------|--------------|------------------------------------------|
| 1    | Joystick     | Analog control using the joystick        |
| 2    | UART2        | Voice command input (e.g., `"left"`)     |
| 3    | UART3        | Face/eye-based commands from AI system   |
| 4    | UART3 (alt)  | Alternative UART3 control logic          |

---

## 🧠 UART Command System

- Receives character-by-character input
- Recognizes strings like `"left"`, `"right"`, `"up"`, `"down"`
- Executes corresponding movement functions

---

## 📡 Pin Configuration

### Inputs

| Pin     | Purpose                  |
|---------|--------------------------|
| `PA4`   | Mode 1 – Joystick        |
| `PA5`   | Mode 2 – Voice via UART2 |
| `PA6`   | Mode 3 – Face via UART3  |
| `PA7`   | Mode 4 – Eye via UART3   |

### Outputs

| Pin       | Description             |
|-----------|--------------------------|
| `PB0/1`   | Motor A control pins     |
| `PB12/13` | Motor B control pins     |
| `PC13`    | Status LED (blinking)    |

---

## 🛠️ File Structure

| File        | Description                        |
|-------------|------------------------------------|
| `main.c`    | Firmware logic                     |
| `README.md` | Documentation (this file)          |

---

## 🧑‍💻 Developed By

- **Eng. Mostafa Salama** – Embedded systems, joystick ADC interface, UART parsing, motor control logic

---

## 📌 Notes

- STM32 UART Baud Rate: `9600`
- HAL Library used for hardware abstraction
- Supports smooth transition between multiple modes

---

> “Empowering mobility through smart, embedded intelligence.”

