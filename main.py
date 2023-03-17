import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.fft import fft, fftfreq, fftshift
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Variables initialization
sampler = 44100
blocksize=1024
audio_buffer = []

# Set up Tkinter UI
root = tk.Tk()
root.title("Autrum")

#### Graph section #####
graph_frame = ttk.Frame(root)
graph_frame.pack(side=tk.TOP, padx=10, pady=10)

# Time Graph
time_label = ttk.Label(graph_frame, text="Time Domain")
time_label.grid(row=0, column=0, padx=10, pady=5)

fig_time = plt.Figure(figsize=(5, 4), dpi=100)
ax_time = fig_time.add_subplot(111)
line_time, = ax_time.plot([])
canvas_time = FigureCanvasTkAgg(fig_time, master=graph_frame)
canvas_time.draw()
canvas_time.get_tk_widget().grid(row=1, column=0, padx=10, pady=0)

# Freq Graph
freq_label = ttk.Label(graph_frame, text="Frequency Domain")
freq_label.grid(row=0, column=1, padx=10, pady=5)

fig_freq = plt.Figure(figsize=(5, 4), dpi=100)
ax_freq = fig_freq.add_subplot(111)
line_freq, = ax_freq.plot([])
canvas_freq = FigureCanvasTkAgg(fig_freq, master=graph_frame)
canvas_freq.draw()
canvas_freq.get_tk_widget().grid(row=1, column=1, padx=10, pady=0)


#### Recording section #####
record_frame = ttk.Frame(root)
record_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

# Load icon images for user buttons
icon_image = Image.open("assets/noun-mic-5589562.png")
icon_image = icon_image.resize((32, 32))
icon_mic = ImageTk.PhotoImage(icon_image)

icon_image = Image.open("assets/noun-play-5587571.png")
icon_image = icon_image.resize((32, 32))
icon_play = ImageTk.PhotoImage(icon_image)

icon_image = Image.open("assets/noun-stop-1152678.png")
icon_image = icon_image.resize((32, 32))
icon_stop = ImageTk.PhotoImage(icon_image)

# Render buttons with labels
record_button = ttk.Button(record_frame, image=icon_mic)
record_button.grid(row=0, column=0, padx=10, pady=0)
record_label = ttk.Label(record_frame, text="Record")
record_label.grid(row=1, column=0, padx=10, pady=0)

play_button = ttk.Button(record_frame, image=icon_play)
play_button.grid(row=0, column=1, padx=10, pady=0)
play_button.config(state="disabled")
play_label = ttk.Label(record_frame, text="Play")
play_label.grid(row=1, column=1, padx=10, pady=0)

# Function definition

def audio_callback(indata, frames, time, status):
    audio_buffer.extend(indata[:, 0])

    # Updates time domain graph
    line_time.set_data(range(len(audio_buffer)), audio_buffer)
    ax_time.relim()
    ax_time.autoscale_view()
    canvas_time.draw()

    # Updates frequency domain graph
    window = np.hamming(len(audio_buffer))
    spectrum = np.abs(fftshift(fft(window * audio_buffer)))
    freqs = fftshift(fftfreq(len(audio_buffer), 1/sampler))
    line_freq.set_data(freqs, spectrum)
    ax_freq.relim()
    ax_freq.autoscale_view()
    canvas_freq.draw()

def start_recording():
    global audio_buffer

    # Stops or starts the recording
    if stream.active:
        record_button.configure(image=icon_mic)
        stream.stop()
    else:
        record_button.configure(image=icon_stop)
        audio_buffer = []
        stream.start()

def play_audio():
    # Replays the recorded audio
    sd.play(audio_buffer, sampler)

# Set up button callbacks
record_button.configure(command=start_recording)
play_button.configure(command=play_audio)

stream = sd.InputStream(callback=audio_callback, channels=1, blocksize=2048, samplerate=sampler)
root.mainloop()
