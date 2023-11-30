import cv2
from datetime import datetime as dt, timedelta
import threading
import pygame
import time

# Initialize Pygame for audio playback
pygame.init()

# Christmas carol file path (replace 'Angels We Have Heard On High.mp3' with the actual file path)
christmas_carol_path = 'carol.mp3'

# Open the USB camera and create a capture object
cap = cv2.VideoCapture(0)

# Set camera resolution to 1280x720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Load the classifier for face detection
face_cascade = cv2.CascadeClassifier('face_detector.xml')

# Create a large-sized window
cv2.namedWindow('Camera Display', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Camera Display', 1280, 720)  # Adjust to desired size

# Initialize variables
carol_play_flag = False
carol_play_duration = timedelta(seconds=30)
merry_christmas_message = ""
last_detected_time = dt.now()
music_playing = False  # Flag to check if music is currently playing


# Function to load and play Christmas carol
def play_christmas_carol():
    global music_playing
    music_playing = True
    pygame.mixer.music.load(christmas_carol_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    music_playing = False


# Timer thread function
def timer():
    global carol_play_flag, last_detected_time
    threading.Timer(1.0, timer).start()

    if carol_play_flag and not music_playing:
        play_christmas_carol()


# Start the timer
timer_thread = threading.Thread(target=timer)
timer_thread.start()

while True:
    # Read frames from the camera
    ret, frame = cap.read()

    # Exit if frames are not read properly
    if not ret:
        break

    # Check if music is playing, if so, skip face detection
    if music_playing:
        # Display Merry Christmas message
        merry_christmas_message = "Merry Christmas!"
        cv2.putText(frame, merry_christmas_message, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    else:
        # Face detection
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=4)

        # Draw rectangles around detected faces and display debug messages
        for (x, y, w, h) in faces:
            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display debug message
            debug_message = f"Person Detected at ({x + w // 2}, {y + h // 2})"
            cv2.putText(frame, debug_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Set the flag to play the carol for an extended duration
            carol_play_flag = True

            # Update the last_detected_time
            last_detected_time = dt.now()

    # Check if carol play duration has passed
    if carol_play_flag and (dt.now() - last_detected_time) > carol_play_duration:
        carol_play_flag = False

    # Display frames in the large-sized window
    cv2.imshow('Camera Display', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
