import os
import pyaudio

import resources.strings as st
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk
from scipy.fft import fft, fftfreq, fftshift
from scipy.io.wavfile import read, write
from tkinter import filedialog, ttk


# Variables initialization
blocksize=1024
sampler = 44100
audio_buffer = []
out_dir = "out/"
temp_dir = "temp/"

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

file_label = ttk.Label(record_frame, text=st.file_selected_label)
file_label.grid(row=0, column=3, padx=10)

### Function definition ###

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
        save_atm()
    else:
        record_button.configure(image=icon_stop)
        audio_buffer = []
        stream.start()

def play_audio():
    sd.play(audio_buffer, sampler)

def save_atm():
    np.save(out_dir+st.atm_output_file, audio_buffer)
    os.replace(out_dir+st.atm_output_file+".npy", out_dir+st.atm_output_file)

def load_audio():
    global audio_buffer
    
    audio_data = np.load(out_dir+st.atm_output_file, 'r')
    write(temp_dir+st.temp_audio_file, sampler, audio_data)
    sampler, data = read(temp_dir+st.temp_audio_file)
    audio_buffer = audio_data

    # Plays the audio data using PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(data.dtype.itemsize),
                    channels=len(data.shape),
                    rate=sampler,
                    output=True)
    stream.write(data.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

def open_file():
    filetypes = (
        ('autrum files', '*.atm'),
        ('All files', '*.*')
    )
    current_dir = os.getcwd()+out_dir
    file_path = filedialog.askopenfilename(filetypes=filetypes, initialdir=current_dir)

    # Check if a file was selected
    if file_path:
        file_label.config(text=st.file_selected_label+file_path)
    else:
        file_label.config(text=st.file_not_selected_label)


# Set up button callbacks
record_button.configure(command=start_recording)
play_button.configure(command=play_audio)
open_button.configure(command=open_file)

stream = sd.InputStream(samplerate=sampler, blocksize=2048, channels=1, callback=audio_callback)
root.mainloop()
