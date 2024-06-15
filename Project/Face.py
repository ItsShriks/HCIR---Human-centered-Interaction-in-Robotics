import cv2
import dlib
import time
import os

# Initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector()

# Function to calculate probability of face detection
def face_detection_probability(dets, scores, idx):
    if len(dets) == 0:
        return 0.0
    return scores[0]

# Path to the success image
success_image_path = "Media/Success.001.jpeg"  # Change this to your image path

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

# Variables to track probability duration and success display time
probability_above_100_start_time = None
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

    # Convert frame to grayscale as dlib works with grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces and get scores
    dets, scores, idx = detector.run(gray, 1)

    # Draw rectangle around each face and calculate probability
    for i, d in enumerate(dets):
        x, y, w, h = d.left(), d.top(), d.width(), d.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Calculate the highest probability
    probability = face_detection_probability(dets, scores, idx) * 100

    # Display probability on the frame
    cv2.putText(frame, f'Probability: {probability:.2f}%', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display message if probability is below 50%
    if probability < 50:
        cv2.putText(frame, 'Come Closer', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Check if probability stays above 100% for more than 5 seconds
    current_time = time.time()
    if probability > 100:
        if probability_above_100_start_time is None:
            probability_above_100_start_time = current_time
        elif (current_time - probability_above_100_start_time) > 5:
            if not success_displayed:
                success_display_start_time = current_time
                success_displayed = True
                # Break the loop to stop displaying webcam feed
                break
    else:
        probability_above_100_start_time = None

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
