import cv2
import mediapipe as mp
import numpy as np
from saving_trajectory import save_trajectory
from ui import ui

# Using FineCam as Webcam (index 1)

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.4)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)

# Variables
mode = "view"
brush_color = (255, 255, 255)
color_pressed = 0
canvas = None
points = []
prev_x, prev_y = None, None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # Define drawing area by a rectangle (370, 225) to (841, 571)
    cv2.rectangle(frame, (370, 225), (841, 571), (255, 0, 0), 2)

    if result.multi_hand_landmarks and mode != "view":
        for hand_landmarks in result.multi_hand_landmarks:
            h, w, c = frame.shape

            index = hand_landmarks.landmark[8]
            x = int(index.x * w)
            y = int(index.y * h)
            print(f"Index finger: ({x}, {y})")

            if x < 841 and y < 571 and y > 225 and x > 370:
                if prev_x is not None and prev_y is not None:
                    if mode == "draw":
                        cv2.line(canvas, (prev_x, prev_y), (x, y), brush_color, 5)
                    elif mode == "eraser":
                        cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 0), 20)

                prev_x, prev_y = x, y
                points.append((x, y))

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        prev_x, prev_y = None, None 

    ui(frame, mode)

    # Combine frame + canvas
    combined = cv2.add(frame, canvas)
    cv2.imshow("Draw with index", combined)

    key = cv2.waitKey(1)
    # Quit
    if key == ord('q'):
        break
    
    # Save trajectory and simplified trajectory
    elif key == ord('s'):
        save_trajectory(points, frame)

    # Change mode
    elif key == ord('d'):
        mode = "view"
    elif key == ord('w'):
        mode = "draw"
    elif key == ord('x'):
        mode = "eraser"

    # Change color (doesn't affect trajectory, only drawing)
    elif key == ord('a'):
        b_to_c = [(255, 0, 255),  # Magenta
                  (255, 0, 0),    # Blue    
                  (0, 255, 0),    # Green
                  (0, 255, 255),  # Yellow
                  (0, 0, 255)]    # Red
        brush_color = b_to_c[color_pressed]
        if color_pressed < len(b_to_c) - 1:
            color_pressed += 1
        else:
            color_pressed = 0

    # Save drawing and clear canvas
    elif key == ord('c'):
        points = []
        cv2.imwrite("drawing.png", canvas)
        print("Saved drawing.png")
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()
