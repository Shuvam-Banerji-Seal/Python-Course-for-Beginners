import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import matplotlib.animation as animation

# Define two 3D vectors
u = np.array([1, 2, 3])
v = np.array([4, 5, 6])
w = u + v

# Create a figure and a 3D axis
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_zlim(0, 10)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Vector Addition')

# Initialize lines for vectors u, v, and w (u + v) using ax.plot
line_u, = ax.plot([], [], [], 'r-', lw=2, label='u = [1, 2, 3]')
line_v, = ax.plot([], [], [], 'g-', lw=2, label='v = [4, 5, 6]')
line_w, = ax.plot([], [], [], 'b-', lw=2, label='u + v = [5, 7, 9]')
ax.legend()

def init():
    line_u.set_data([], [])
    line_u.set_3d_properties([])
    line_v.set_data([], [])
    line_v.set_3d_properties([])
    line_w.set_data([], [])
    line_w.set_3d_properties([])
    return line_u, line_v, line_w,

def animate(i):
    i = i + 1  # i goes from 0 to 99, so we need it to go from 1 to 100
    if i > 100:
        i = 100
    
    # Animate vector u
    x_u = np.linspace(0, u[0] * i / 100, 100)
    y_u = np.linspace(0, u[1] * i / 100, 100)
    z_u = np.linspace(0, u[2] * i / 100, 100)
    line_u.set_data(x_u[:i], y_u[:i])
    line_u.set_3d_properties(z_u[:i])
    
    # Animate vector v (starts from the tip of u)
    x_v = np.linspace(u[0], u[0] + v[0] * i / 100, 100)
    y_v = np.linspace(u[1], u[1] + v[1] * i / 100, 100)
    z_v = np.linspace(u[2], u[2] + v[2] * i / 100, 100)
    line_v.set_data(x_v[:i], y_v[:i])
    line_v.set_3d_properties(z_v[:i])
    
    # Animate vector w (u + v) directly from origin to w
    x_w = np.linspace(0, w[0] * i / 100, 100)
    y_w = np.linspace(0, w[1] * i / 100, 100)
    z_w = np.linspace(0, w[2] * i / 100, 100)
    line_w.set_data(x_w[:i], y_w[:i])
    line_w.set_3d_properties(z_w[:i])
    
    return line_u, line_v, line_w,

# Call the animator
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=50, blit=True)

# Save the animation if necessary
# ani.save('vector_addition_3d_animation.mp4', writer='ffmpeg', fps=30)

plt.show()
