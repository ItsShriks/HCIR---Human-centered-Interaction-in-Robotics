import cv2
import time
import os
import concurrent.futures
from qibullet import SimulationManager, PepperVirtual
from gtts import gTTS
from playsound import playsound

# Load the pre-trained Haar cascades classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Path to the success image
success_image_path = "../Media/Success.001.jpeg"  # Change this to your image path

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

# Variables to track probability duration and success display time
face_detected_start_time = None
success_display_start_time = None
success_displayed = False

# Function to show image full screen
def show_full_screen(image, window_name):
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, image)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale as Haar cascades work with grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Determine if a face is detected
    if len(faces) > 0:
        face_detected = True
    else:
        face_detected = False

    # Display probability on the frame
    if face_detected:
        cv2.putText(frame, f'Face Detected', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, 'No Face Detected', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Check if a face is detected for more than 2 seconds
    current_time = time.time()
    if face_detected:
        if face_detected_start_time is None:
            face_detected_start_time = current_time
        elif (current_time - face_detected_start_time) > 2:
            if not success_displayed:
                success_display_start_time = current_time
                success_displayed = True
                # Break the loop to stop displaying webcam feed
                break
    else:
        face_detected_start_time = None

    # Display the resulting frame in full screen
    show_full_screen(frame, 'Face Detection')

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the webcam window
cv2.destroyWindow('Face Detection')

# Load and display the success image
if success_displayed:
    success_image = cv2.imread(success_image_path)
    if success_image is not None:
        show_full_screen(success_image, 'Success')
        cv2.waitKey(5000)  # Display for 5 seconds

# Close all windows
cv2.destroyAllWindows()
# Release the capture
cap.release()

# Functions for Pepper robot greetings
def wave(pepper):
    for _ in range(2):
        pepper.setAngles("RShoulderPitch", -0.5, 0.5)
        pepper.setAngles("RShoulderRoll", -1.5620, 0.5)
        pepper.setAngles("RElbowRoll", 1.5620, 0.5)
        time.sleep(1.0)
        pepper.setAngles("RElbowRoll", -1.5620, 0.5)
        time.sleep(1.0)

def normal(pepper):
    pepper.goToPosture("StandInit", 0.6)
    time.sleep(1.0)

def speak(message, filename):
    tts = gTTS(message)
    tts.save(filename)
    playsound(filename)

def head_nod(pepper):
    for _ in range(2):
        pepper.setAngles("HeadPitch", 0.5, 0.5)  # Nod down
        time.sleep(1.0)
        pepper.setAngles("HeadPitch", -0.5, 0.5)  # Nod up
        time.sleep(1.0)

# Start Pepper robot simulation and perform greetings
if success_displayed:
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    pepper.goToPosture("Crouch", 0.6)
    time.sleep(1)
    pepper.goToPosture("StandInit", 0.6)
    time.sleep(1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_wave = executor.submit(wave, pepper)
        future_speak = executor.submit(speak, "Hello MAS Students", "message.mp3")
        concurrent.futures.wait([future_wave, future_speak])

        future_normal = executor.submit(normal, pepper)
        concurrent.futures.wait([future_normal])

        future_speak_2 = executor.submit(speak, "Glad to see you", "message1.mp3")
        future_nod = executor.submit(head_nod, pepper)
        concurrent.futures.wait([future_speak_2, future_nod])

        # Run speak_3 and head_nod together
        future_speak_3 = executor.submit(speak, "Lets now move towards the selection of elective subjects", "message2.mp3")
        future_nod_again = executor.submit(head_nod, pepper)
        concurrent.futures.wait([future_speak_3, future_nod_again])

    simulation_manager.stopSimulation(client)

