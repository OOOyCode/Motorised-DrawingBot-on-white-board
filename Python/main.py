import cv2
import mediapipe as mp
import numpy as np
from saving_trajectory import save_trajectory
from ui import ui
from menu import Menu

user_menu = Menu()

mode = user_menu.get_mode()
settings = user_menu.get_settings()

print(mode, settings)
r = settings["color"][2]
g = settings["color"][1]
b = settings["color"][0]

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.4)
mp_draw = mp.solutions.drawing_utils

try:
    cap = cv2.VideoCapture(1)
except:
    cap = cv2.VideoCapture(0)

# Variables
mode = "view"
brush_color = settings["color"]
width = settings["width"]
color_pressed = 0
canvas = None
points = []
prev_x, prev_y = None, None

def nothing(x):
    pass
cv2.namedWindow("Controls")

cv2.createTrackbar("R", "Controls", r, 255, nothing)
cv2.createTrackbar("G", "Controls", g, 255, nothing)
cv2.createTrackbar("B", "Controls", b, 255, nothing)
cv2.createTrackbar("Width", "Controls", width, 50, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    
    cv2.rectangle(frame, (370, 225), (841, 571), (255, 0, 0), 2)

    r = cv2.getTrackbarPos("R", "Controls")
    g = cv2.getTrackbarPos("G", "Controls")
    b = cv2.getTrackbarPos("B", "Controls")
    width = cv2.getTrackbarPos("Width", "Controls")

    brush_color = (b, g, r)

    if result.multi_hand_landmarks and mode != "view":
        for hand_landmarks in result.multi_hand_landmarks:
            h, w, c = frame.shape

            index = hand_landmarks.landmark[8]
            x = int(index.x * w)
            y = int(index.y * h)
            if mode == "Trajectoire":
                x = round(x, -1)
                y = round(y, -1)
            print(f"Index finger: ({x}, {y})")

            if x < 841 and y < 571 and y > 225 and x > 370:
                
                if prev_x is not None and prev_y is not None:
                    if mode == "draw":
                        cv2.line(canvas, (prev_x, prev_y), (x, y), brush_color,  thickness=width)
                    elif mode == "eraser":
                        cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 0),  thickness=width)

                prev_x, prev_y = x, y
                points.append((x, y))

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        prev_x, prev_y = None, None 

    ui(frame, mode, r, g, b)

    combined = cv2.add(frame, canvas)
    cv2.imshow("Draw with index", combined)

    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
    
    elif key == ord('s'):
        save_trajectory(points, frame)

    # Change mode
    elif key == ord('d'):
        mode = "view"
    elif key == ord('w'):
        mode = "draw"
    elif key == ord('x'):
        mode = "eraser"

    elif key == ord('c'):
        points = []
        cv2.imwrite("drawing.png", canvas)
        print("Saved drawing.png")
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()
