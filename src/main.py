import serial.tools.list_ports
import mediapipe as mp
import cv2

cam = cv2.VideoCapture(0)  # Open the default webcam

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()  # Initialize MediaPipe Hands model
mp_drawing = mp.solutions.drawing_utils

try:
    serial = serial.Serial()
    serial.baudrate = 9600   # Baud rate for Arduino serial communication (must match the sketch)
    serial.port = "COM3"     # Update!!! this based on which COM port the Arduino is using
    serial.open()
except Exception as e:
    print(f'Error: {e}')
    exit()

while cam.isOpened():

    success, frame = cam.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)  # Flip horizontally for mirror view

    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for MediaPipe
    multi_landmark = result.multi_hand_landmarks

    if multi_landmark:
        for hand_landmark, multi_handedness in zip(multi_landmark, result.multi_handedness):
            mp_drawing.draw_landmarks(
                frame,
                hand_landmark,
                mp_hand.HAND_CONNECTIONS
            )

            # Check if each finger is raised by finger joint coordinates
            thumb = hand_landmark.landmark[3].x > hand_landmark.landmark[4].x
            index = hand_landmark.landmark[6].y > hand_landmark.landmark[8].y
            middle = hand_landmark.landmark[10].y > hand_landmark.landmark[12].y
            ring = hand_landmark.landmark[14].y > hand_landmark.landmark[16].y
            pinky = hand_landmark.landmark[18].y > hand_landmark.landmark[20].y 

            # Detect handedness to adjust thumb logic for left hand
            label = multi_handedness.classification[0].label
            if label == 'Left':
                thumb = not thumb

            # If all five fingers are raised, send "1" (ON), else send "0" (OFF)
            if all([thumb, index, middle, ring, pinky]):
                command = "1"
            else:
                command = "0"

        # Debug print lines for finger detection (optional)
        # if thumb:
        #     print('Thumb')
        # if index:
        #     print('Index')
        # if middle:
        #     print('Middle')
        # if ring:
        #     print('Ring')
        # if pinky:
        #     print('Pinky')

        serial.write(command.encode('utf-8'))  # Send command to Arduino

    cv2.imshow("Hand Tracker", frame)
    if cv2.waitKey(1) == 27:  # Press ESC to exit
        break

cam.release()
cv2.destroyAllWindows()
