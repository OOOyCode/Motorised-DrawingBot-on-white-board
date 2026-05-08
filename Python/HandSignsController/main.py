import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial('COM7', 9600) 
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
finger_joints = [6, 10, 14, 18]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    hands_open = [0] * 8

    if result.multi_hand_landmarks:
        for hand_id, hand_landmarks in enumerate(result.multi_hand_landmarks):

            if hand_id >= 2:
                break  # sécurité

            for i in range(4):
                tip = hand_landmarks.landmark[finger_tips[i]]
                joint = hand_landmarks.landmark[finger_joints[i]]

                if tip.y < joint.y:
                    hands_open[hand_id * 4 + i] = 1
                else:
                    hands_open[hand_id * 4 + i] = 0

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    binary_string = ''.join(map(str, hands_open))

    print(binary_string)

    # ===== envoyer à Arduino =====
    arduino.write((binary_string + "\n").encode())

    cv2.putText(frame, binary_string, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hands", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
