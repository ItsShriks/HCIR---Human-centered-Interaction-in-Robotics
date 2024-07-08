import cv2
import time
import os
import subprocess
from qibullet import SimulationManager, PepperVirtual
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import requests
import threading
import webbrowser

# Load the pre-trained Haar cascades classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Path to the success image
success_image_path = "Media/Success.001.jpeg"  # Change this to your image path

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

# Variables to track probability duration and success display time
face_detected_start_time = None
success_display_start_time = None
success_displayed = False

# Rasa server URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

# Function to show image full screen
def show_full_screen(image, window_name):
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, image)

# Function to communicate with Rasa and get response
def get_rasa_response(message):
    payload = {
        "sender": "user",
        "message": message
    }
    response = requests.post(RASA_SERVER_URL, json=payload)
    return response.json()

# Function to make Pepper speak using TTS
def speak(message, filename):
    tts = gTTS(message)
    tts.save(filename)
    audio = AudioSegment.from_mp3(filename)
    play(audio)
    os.remove(filename)  # Optionally remove the temporary file after playing

# Functions for Pepper robot greetings and interactions
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

def head_nod(pepper):
    for _ in range(2):
        pepper.setAngles("HeadPitch", 0.5, 0.5)  # Nod down
        time.sleep(1.0)
        pepper.setAngles("HeadPitch", -0.5, 0.5)  # Nod up
        time.sleep(1.0)

# Function to open the HTML chat interface
def open_chat_html():
    # Open the HTML file in the default web browser
    webbrowser.open("chat.html")

# Function to speak asynchronously
def speak_async(message, filename):
    threading.Thread(target=speak, args=(message, filename)).start()

# Pepper robot interaction sequence
def pepper_interaction(pepper):
    # Pepper's initial greeting
    wave(pepper)
    speak("Hello M A S Students", "message.mp3")
    normal(pepper)
    speak("Glad to see you", "message1.mp3")
    head_nod(pepper)

    # Ask the user how they want to chat
    chat_choice = input("Do you want to chat in the audio or chatbox? (type 'audiochat' or 'chatbox'): ").strip().lower()
    use_chatbox = chat_choice == 'chatbox'

    if use_chatbox:
        # Open the HTML chat interface in a separate thread
        threading.Thread(target=open_chat_html).start()

    # Rasa interaction loop
    while True:
        if use_chatbox:
            user_input = input("You (Chatbox - type 'done' to switch): ")
            if user_input.lower() == 'done':
                speak("Switching to audio chat.", "switch.mp3")
                use_chatbox = False
                continue
        else:
            user_input = input("You: ")
            if user_input.lower() in ['chatbox', 'switch']:
                speak("Switching to chatbox.", "switch.mp3")
                open_chat_html()
                use_chatbox = True
                continue

        if user_input.lower() in ['bye', 'goodbye', 'stop']:
            speak("Goodbye!", "goodbye.mp3")
            head_nod(pepper)
            break

        rasa_response = get_rasa_response(user_input)
        if rasa_response:
            pepper_response = rasa_response[0].get("text", "Sorry, I didn't understand that.")
            print(f"Pepper: {pepper_response}")
            speak_async(pepper_response, "pepper_response.mp3")
            head_nod(pepper)

# Main facial detection loop
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
    face_detected = len(faces) > 0

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

# Start Pepper robot simulation and perform greetings
if success_displayed:
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    pepper.goToPosture("Crouch", 0.6)
    time.sleep(1)
    pepper.goToPosture("StandInit", 0.6)
    time.sleep(1)

    pepper_interaction(pepper)

    # Keep the simulation running until the user closes it
    input("Press Enter to stop the simulation...")
    simulation_manager.stopSimulation(client)
