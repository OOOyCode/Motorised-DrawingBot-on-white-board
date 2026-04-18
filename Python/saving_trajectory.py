import numpy as np
from algo_rdp import rdp
import cv2

def save_trajectory(points, frame):
        if len(points) > 10:
            simplified = rdp(points, epsilon=5)

            np.save("trajectory.npy", np.array(simplified))

            img = np.ones((frame.shape[0], frame.shape[1], 3), dtype=np.uint8) * 255

            pts = np.array(simplified, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))

            cv2.polylines(img, [pts], isClosed=False, color=(0, 0, 0), thickness=1)

            cv2.imwrite("trajectory.png", img)

            print("Saved trajectory.png + trajectory.npy")
            print("Points:", len(points), "========", len(simplified))
            print("_________________________________________________")

        else:
            print("Not enough points")
