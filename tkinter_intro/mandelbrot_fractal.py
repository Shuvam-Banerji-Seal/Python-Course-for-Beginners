import tkinter as tk
import math
from tkinter import messagebox

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n

def draw_mandelbrot(canvas, width, height, max_iter):
    for x in range(width):
        for y in range(height):
            real = (x - width / 2) *4.0 / width
            imag = (y - height / 2) * 4.0 / height
            c = complex(real, imag)
            m = mandelbrot(c, max_iter)

            color = "black" if m == max_iter else f"#{m%256:02x}{m%256:02x}{m%256:02x}"
            canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline=color)


def create_mandelbrot_fractal():
    fractal_window = tk.Toplevel(root)
    fractal_window.title("Mandelbrot Fractal")
    # fractal_window.geometry("800x600")
    width = 800
    height = 600
    max_iter = 100

    canvas = tk.Canvas(fractal_window, width=width, height=height, bg="white")
    canvas.pack()

    draw_mandelbrot(canvas, width, height, max_iter)

root = tk.Tk()
root.title("Mandelbrot Fractal Generator")
root.geometry("300x200")
fractal_button = tk.Button(root, text="Generate Mandelbrot Fractal", command=create_mandelbrot_fractal)
fractal_button.pack(pady=50)

root.mainloop()
