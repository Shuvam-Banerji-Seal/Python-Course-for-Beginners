import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)
point, = ax.plot([], [], 'ro')

z = 1 + 1j  # initial complex number

def update(frame):
    theta = np.radians(frame)
    rotated = z * np.exp(1j * theta)
    point.set_data([rotated.real], [rotated.imag])
    return point,

ani = animation.FuncAnimation(fig, update, frames=360, interval=30, blit=True)
plt.title("Rotating Complex Number")
plt.show()
