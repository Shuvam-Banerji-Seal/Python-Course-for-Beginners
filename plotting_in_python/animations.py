import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# fig, ax = plt.subplots()
# x = np.linspace(0, 2 * np.pi, 100)
# line, = ax.plot(x, np.sin(x), color='blue')

# ax.set_ylim(-1.5, 1.5)
# ax.set_title("Sine Wave Animation")

# def update(frame):
#     line.set_ydata(np.sin(x + frame / 100.0)) #shifting the sine wave
#     print(type(line))  # This will print the type of line
#     return line,

# ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
# plt.show()


# fig, ax = plt.subplots()
# x = np.linspace(0, 4*np.pi, 300)
# line, = ax.plot(x, np.exp(-x)*np.sin(x))
# ax.set_ylim(-1, 1)

# def update(frame):
#     y = np.exp(-x) * np.sin(x + frame / 10)
#     line.set_ydata(y)
#     return line,

# ani = animation.FuncAnimation(fig, update, frames=100, interval=60, blit=True)
# plt.title("Damped Oscillation Animation")
# plt.show()


fig, ax = plt.subplots()
x = np.linspace(-100, 100, 2000)
line, = ax.plot(x, x**2)

def update(frame):
    line.set_ydata((x**2) * (frame / 500))  # Scale quadratic curve
    return line,

ax.set_ylim(0, 20000)
plt.title("Growing Parabola")
ani = animation.FuncAnimation(fig, update, frames=500, interval=10, blit=True)
plt.grid(True)
plt.show()
