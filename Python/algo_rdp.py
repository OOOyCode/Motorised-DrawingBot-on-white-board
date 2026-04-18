import numpy as np

# Ramer-Douglas-Peucker algorithm for trajectory simplification
def rdp(points, epsilon):
    if len(points) < 3:
        return points

    start = np.array(points[0])
    end = np.array(points[-1])

    line = end - start
    line_norm = np.linalg.norm(line)

    max_dist = 0
    index = 0

    for i in range(1, len(points) - 1):
        p = np.array(points[i])

        if line_norm == 0:
            dist = np.linalg.norm(p - start)
        else:
            dist = np.abs(np.cross(line, start - p)) / line_norm

        if dist > max_dist:
            max_dist = dist
            index = i

    if max_dist > epsilon:
        left = rdp(points[:index+1], epsilon)
        right = rdp(points[index:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]
