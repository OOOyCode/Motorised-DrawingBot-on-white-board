import cv2

def ui(frame, mode):
    cv2.rectangle(frame, (5, 5), (300, 350), (0, 0, 0), -1)

    cv2.putText(frame, f"Mode: {mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"View Mode: 'D'", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Draw Mode: 'W'", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Eraser Mode: 'X'", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Save: 'S'", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Quit Mode: 'Q'", (10, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
