import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import os

def plot_summary(t, drive, x, y, z, pur, c1, save_dir="results/figures"):
    os.makedirs(save_dir, exist_ok=True)
    fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)
    axs[0].plot(t, drive)
    axs[0].set_ylabel("drive")
    axs[1].plot(t, x, label="x")
    axs[1].plot(t, y, label="y")
    axs[1].plot(t, z, label="z")
    axs[1].legend()
    axs[1].set_ylabel("bloch")
    axs[2].plot(t, pur)
    axs[2].set_ylabel("purity")
    axs[3].plot(t, c1)
    axs[3].set_ylabel("l1")
    axs[3].set_xlabel("time")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "summary.png"))
    plt.close()

def animate_bloch(t, x, y, z, save_dir="results/figures"):
    os.makedirs(save_dir, exist_ok=True)
    fig, ax = plt.subplots()
    line_x, = ax.plot([], [], label="x")
    line_y, = ax.plot([], [], label="y")
    line_z, = ax.plot([], [], label="z")
    ax.set_xlim(0, t[-1])
    ax.set_ylim(-1, 1)
    ax.legend()

    def init():
        line_x.set_data([], [])
        line_y.set_data([], [])
        line_z.set_data([], [])
        return line_x, line_y, line_z

    def update(frame):
        line_x.set_data(t[:frame], x[:frame])
        line_y.set_data(t[:frame], y[:frame])
        line_z.set_data(t[:frame], z[:frame])
        return line_x, line_y, line_z

    ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=30)
    ani.save(os.path.join(save_dir, "bloch_animation.gif"), writer="pillow")
    plt.close()

def animate_bloch_sphere(x, y, z, save_dir="results/figures"):
    os.makedirs(save_dir, exist_ok=True)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    line, = ax.plot([], [], [], lw=2)
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])

    def update_sphere(frame):
        line.set_data(x[:frame], y[:frame])
        line.set_3d_properties(z[:frame])
        return line,

    ani = FuncAnimation(fig, update_sphere, frames=len(x), blit=True, interval=30)
    ani.save(os.path.join(save_dir, "bloch_sphere.gif"), writer="pillow")
    plt.close()
