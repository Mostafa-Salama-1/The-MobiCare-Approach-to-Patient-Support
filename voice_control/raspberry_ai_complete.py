import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
import warnings
warnings.filterwarnings('ignore')  # Suppress other warnings
import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd
import librosa
import time
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
import serial
import sys
import threading
import queue

# ---------------- UART CONFIGURATION ----------------
SERIAL_PORT = '/dev/ttyAMA0'  # Hardware UART on Raspberry Pi 4
# Alternative ports: '/dev/ttyS0' or '/dev/serial0'
BAUD_RATE = 9600

# ---------------- VOICE MODEL CONFIGURATION ----------------
SAMPLING_RATE = 8000
DURATION = 1.0  # 1 sec
N_MELS = 64
CLASSES = ['backward', 'forward', 'left', 'right', 'stop']
THRESHOLD = 0.70  # threshold 70%
voice_model = load_model("best_model_f2.keras")
scaler = StandardScaler()

def extract_features(audio):
    audio = librosa.util.fix_length(audio, size=8000)
    mel = librosa.feature.melspectrogram(y=audio, sr=SAMPLING_RATE, n_mels=N_MELS)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = mel_db.T
    mel_db = scaler.fit_transform(mel_db)
    return np.expand_dims(mel_db, axis=0)

def run_voice_detection():
    print("Listening for voice command...")
    try:
        recording = sd.rec(int(DURATION * SAMPLING_RATE), samplerate=SAMPLING_RATE, channels=1, dtype='float32')
        sd.wait()
        print("Audio recorded. Shape:", recording.shape)
        audio = recording.flatten()
        features = extract_features(audio)
        print("Features extracted. Shape:", features.shape, "Type:", type(features))
        predictions = voice_model.predict(features)[0]
        print("Predictions:", predictions)
        max_idx = np.argmax(predictions)
        confidence = predictions[max_idx]
        if confidence > THRESHOLD:
            detected = CLASSES[max_idx]
            print(f"Detected: {detected} ({confidence * 100:.2f}%)")
            return detected
        else:
            print("fail confidence < THRESHOLD.")
            return "stop"
    except Exception as e:
        print(f"Voice detection error: {e}")
        return "stop"

# ---------------- FACE MODEL CONFIGURATION ----------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def run_face_detection_stream(send_callback=None, interrupt_callback=None):
    cap = None
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            break
        cap.release()
    if cap is None or not cap.isOpened():
        print("Error: No camera found.")
        return "stop"
    direction = "stop"
    try:
        while True:
            if interrupt_callback and interrupt_callback():
                print("Interrupted by user.")
                direction = "menu"
                break
            success, frame = cap.read()
            if not success:
                print("Error: Failed to read frame from webcam.")
                direction = "stop"
                break
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    x_nose = int(face_landmarks.landmark[5].x * width)
                    y_nose = int(face_landmarks.landmark[5].y * height)
                    x_left_eye = int(face_landmarks.landmark[33].x * width)
                    y_left_eye = int(face_landmarks.landmark[33].y * height)
                    x_right_eye = int(face_landmarks.landmark[263].x * width)
                    y_right_eye = int(face_landmarks.landmark[263].y * height)
                    cv2.circle(frame, (x_nose, y_nose), 5, (255, 100, 0), -1)
                    cv2.circle(frame, (x_left_eye, y_left_eye), 5, (255, 100, 0), -1)
                    cv2.circle(frame, (x_right_eye, y_right_eye), 5, (255, 100, 0), -1)
                    left_nose = abs(x_nose - x_left_eye)
                    right_nose = abs(x_nose - x_right_eye)
                    eye_avg_y = (y_left_eye + y_right_eye) // 2
                    down_threshold = 25
                    if y_nose < eye_avg_y:
                        direction = "up"
                    elif y_nose - eye_avg_y > down_threshold:
                        direction = "down"
                    elif abs(left_nose - right_nose) < 20:
                        direction = "stop"
                    else:
                        direction = "left" if left_nose > right_nose else "right"
                    cv2.putText(frame, direction, (width - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    if send_callback:
                        send_callback(direction)
            cv2.imshow("Face Direction", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"An error occurred: {e}")
        direction = "stop"
    return direction

# ---------------- UART RECEIVER ----------------
def uart_receiver():
    print(f"Opening serial port {SERIAL_PORT} at {BAUD_RATE} baud...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Serial port opened successfully!")
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        print("Available ports:")
        try:
            import glob
            ports = glob.glob('/dev/tty*')
            for port in ports:
                print(f"  {port}")
        except:
            pass
        return None
    
    return ser

# ---------------- MAIN AI PROCESSING ----------------
def process_ai_commands():
    ser = uart_receiver()
    if not ser:
        return
    
    print("Raspberry Pi AI system started. Listening for commands...")
    print("Commands: '3' for voice, '4' for face, 'q' to quit")
    
    active_mode = None
    last_direction = None
    last_sent_time = 0
    
    try:
        while True:
            # Check for incoming commands from STM
            if ser.in_waiting:
                try:
                    cmd = ser.read(1).decode('utf-8').strip()
                    print(f"Received command: {cmd}")
                    
                    if cmd == '3':
                        active_mode = 'voice'
                        print("Switched to voice mode.")
                        ser.write(b'3')  # Send confirmation
                        
                    elif cmd == '4':
                        active_mode = 'face'
                        print("Switched to face mode.")
                        ser.write(b'4')  # Send confirmation
                        
                    elif cmd.lower() == 'q':
                        print("Exiting...")
                        break
                        
                    else:
                        print("Unknown command received.")
                        
                except UnicodeDecodeError:
                    print("Error decoding command")
                except Exception as e:
                    print(f"Error reading command: {e}")
            
            # Process active mode
            if active_mode == 'voice':
                print("Running voice detection...")
                result = run_voice_detection()
                print(f"Voice result: {result}")
                
                # Send direction to STM
                now = time.time()
                if result != last_direction and (now - last_sent_time > 2):
                    ser.write((result + '\n').encode('utf-8'))
                    print(f"Sending direction: {result}")
                    last_direction = result
                    last_sent_time = now
                    
            elif active_mode == 'face':
                print("Running face detection...")
                def send_callback(direction):
                    nonlocal last_direction, last_sent_time
                    now = time.time()
                    if direction != last_direction and (now - last_sent_time > 0.5):
                        ser.write((direction + '\n').encode('utf-8'))
                        print(f"Sending direction: {direction}")
                        last_direction = direction
                        last_sent_time = now
                
                def interrupt_callback():
                    return ser.in_waiting > 0
                
                result = run_face_detection_stream(send_callback=send_callback, interrupt_callback=interrupt_callback)
                print(f"Face detection ended: {result}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nExiting Raspberry Pi AI system...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()
        print("Serial port closed.")

# ---------------- GPIO CONTROL (Optional) ----------------
def setup_gpio():
    """Setup GPIO pins for motor control, LEDs, etc."""
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Example GPIO setup - modify as needed
        # GPIO.setup(18, GPIO.OUT)  # Motor 1
        # GPIO.setup(23, GPIO.OUT)  # Motor 2
        # GPIO.setup(24, GPIO.OUT)  # LED indicator
        
        print("GPIO setup completed")
        return True
    except (ImportError, ModuleNotFoundError):
        print("RPi.GPIO not available - GPIO control disabled")
        return False
    except Exception as e:
        print(f"GPIO setup error: {e}")
        return False

def control_motors(direction):
    """Control motors based on direction command"""
    try:
        import RPi.GPIO as GPIO
        
        # Example motor control - modify according to your setup
        if direction == 'forward':
            # GPIO.output(18, GPIO.HIGH)
            # GPIO.output(23, GPIO.HIGH)
            print("Motors: FORWARD")
        elif direction == 'backward':
            # GPIO.output(18, GPIO.LOW)
            # GPIO.output(23, GPIO.LOW)
            print("Motors: BACKWARD")
        elif direction == 'left':
            # GPIO.output(18, GPIO.HIGH)
            # GPIO.output(23, GPIO.LOW)
            print("Motors: LEFT")
        elif direction == 'right':
            # GPIO.output(18, GPIO.LOW)
            # GPIO.output(23, GPIO.HIGH)
            print("Motors: RIGHT")
        elif direction == 'stop':
            # GPIO.output(18, GPIO.LOW)
            # GPIO.output(23, GPIO.LOW)
            print("Motors: STOP")
            
    except (ImportError, ModuleNotFoundError):
        print("RPi.GPIO not available - motor control disabled")
    except Exception as e:
        print(f"Motor control error: {e}")

if __name__ == "__main__":
    print("=== Raspberry Pi AI System ===")
    print("Initializing...")
    
    # Setup GPIO if available
    gpio_available = setup_gpio()
    
    # Start AI processing
    process_ai_commands()
    
    # Cleanup GPIO
    if gpio_available:
        try:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
            print("GPIO cleanup completed")
        except:
            pass
    
    print("System shutdown complete.") 