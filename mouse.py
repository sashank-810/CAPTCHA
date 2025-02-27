import time
import numpy as np
import matplotlib.pyplot as plt
from Quartz import CGEventCreate, kCGEventMouseMoved
from Quartz.CoreGraphics import CGEventGetLocation

trajectory = []
change_points = []

def get_mouse_position():
    event = CGEventCreate(None)
    return CGEventGetLocation(event)

# Track for 5 seconds
start_time = time.time()
while time.time() - start_time < 5:
    pos = get_mouse_position()
    trajectory.append((pos.x, pos.y))
    time.sleep(0.01)  # 10ms sampling rate

trajectory = np.array(trajectory)

# Detect changes based on slope difference
if len(trajectory) > 2:
    slopes = np.diff(trajectory[:, 1]) / (np.diff(trajectory[:, 0]) + 1e-6)  # Avoid division by zero
    threshold = 1.0  # Adjust this to control sensitivity
    for i in range(1, len(slopes)):
        if abs(slopes[i] - slopes[i - 1]) > threshold:
            point = (float(trajectory[i, 0]), float(trajectory[i, 1]))
            if not change_points or change_points[-1] != point:  # Remove consecutive duplicates
                change_points.append(point)

# Print change points
print("Change points in trajectory:")
for point in change_points:
    print(point)

# **Optional: Plot trajectory**
plt.figure(figsize=(8, 6))
plt.plot(trajectory[:, 0], trajectory[:, 1], label="Mouse Path", color='blue')
plt.scatter(*zip(*change_points), color='red', label="Change Points", zorder=3)
plt.gca().invert_yaxis()  # Flip to match screen coordinates
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.legend()
plt.title("Mouse Movement and Change Points")
plt.show()
