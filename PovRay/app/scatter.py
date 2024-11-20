import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from povview_tracer import Tracer
from povview_math import Vec3

normal = Vec3(0, 1, 0)
random_directions = [
    (normal + Tracer.random_direction()).normalized() for _ in range(1000)
]

x = [direction.x for direction in random_directions]
y = [direction.y for direction in random_directions]
z = [direction.z for direction in random_directions]

# Create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Scatter plot
ax.scatter(x, y, z)

# Set the aspect ratio to be the same for x and y
ax.set_box_aspect([1, 1, 1])  # Aspect ratio for x, y, z

# Manually adjust x and y limits to match each other
max_range = max(max(x) - min(x), max(y) - min(y))
mid_x = (max(x) + min(x)) / 2
mid_y = (max(y) + min(y)) / 2

ax.set_xlim(mid_x - max_range / 2, mid_x + max_range / 2)
ax.set_ylim(mid_y - max_range / 2, mid_y + max_range / 2)

# Labels for axes
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")
ax.set_zlabel("Z Label")

# Title
ax.set_title("3D Scatter Plot")

# Show plot
plt.show()
