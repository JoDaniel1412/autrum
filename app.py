import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk
import resources.strings as st
import tkinter as tk
from tkinter import ttk

# Set up Tkinter UI
root = tk.Tk()
root.title(st.app_title)
root.geometry("1200x600")
root.minsize(1200, 600)

#### Graph section #####
header_frame = ttk.Frame(root)
header_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
header_frame.columnconfigure(0, weight=1)

graph_frame = ttk.Frame(root)
graph_frame.pack(fill=tk.BOTH, expand=True)
graph_frame.rowconfigure(0, weight=1)
graph_frame.columnconfigure(0, weight=1)
graph_frame.grid_propagate(False)

toolbar_frame = ttk.Frame(root)
toolbar_frame.pack(fill=tk.X, expand=True)

# Time Graph
time_label = ttk.Label(header_frame, text=st.time_graph_title, font=('Arial', 18))
time_label.pack(side=tk.LEFT, padx=20)

fig_time = plt.Figure(figsize=(5, 4), dpi=100)
ax_time = fig_time.add_subplot(111)
line_time, = ax_time.plot([])
canvas_time = FigureCanvasTkAgg(fig_time, master=graph_frame)
canvas_time.draw()
canvas_time.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

toolbar = NavigationToolbar2Tk(canvas_time, toolbar_frame)
toolbar.pack(side=tk.LEFT, padx=20)
toolbar.update()

# Freq Graph
freq_label = ttk.Label(header_frame, text=st.freq_graph_title, font=('Arial', 18))
freq_label.pack(side=tk.RIGHT, padx=20)

fig_freq = plt.Figure(figsize=(5, 4), dpi=100)
ax_freq = fig_freq.add_subplot(111)
line_freq, = ax_freq.plot([])
canvas_freq = FigureCanvasTkAgg(fig_freq, master=graph_frame)
canvas_freq.draw()
canvas_freq.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

toolbar = NavigationToolbar2Tk(canvas_freq, toolbar_frame)
toolbar.pack(side=tk.RIGHT, padx=20)
toolbar.update()

#### Recording section #####
record_frame = ttk.Frame(root)
record_frame.pack(side=tk.BOTTOM, padx=10, pady=20)

# Load icon images for user buttons
icon_image = Image.open(st.mic_icon_path)
icon_image = icon_image.resize((32, 32))
icon_mic = ImageTk.PhotoImage(icon_image)

icon_image = Image.open(st.play_icon_path)
icon_image = icon_image.resize((32, 32))
icon_play = ImageTk.PhotoImage(icon_image)

icon_image = Image.open(st.stop_icon_path)
icon_image = icon_image.resize((32, 32))
icon_stop = ImageTk.PhotoImage(icon_image)

icon_image = Image.open(st.open_icon_path)
icon_image = icon_image.resize((32, 32))
icon_open = ImageTk.PhotoImage(icon_image)

# Render buttons with labels
record_button = ttk.Button(record_frame, image=icon_mic)
record_button.grid(row=0, column=0, padx=10)
record_label = ttk.Label(record_frame, text=st.record_btn_label)
record_label.grid(row=1, column=0, padx=10)

play_button = ttk.Button(record_frame, image=icon_play)
play_button.grid(row=0, column=1, padx=10)
play_button.config(state=tk.DISABLED)
play_label = ttk.Label(record_frame, text=st.play_btn_label)
play_label.grid(row=1, column=1, padx=10)

open_button = ttk.Button(record_frame, image=icon_open)
open_button.grid(row=0, column=2, padx=10)
open_label = ttk.Label(record_frame, text=st.open_btn_label)
open_label.grid(row=1, column=2, padx=10)

# Selected file label

file_label = ttk.Label(record_frame, text=st.file_select_label)
file_label.grid(row=0, column=3, padx=10)
