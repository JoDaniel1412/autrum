import datetime
import os

import resources.strings as st
import numpy as np
import sounddevice as sd
import tkinter as tk

from app import *
from scipy.fft import fft, fftfreq, fftshift
from scipy.io.wavfile import write
from tkinter import filedialog


# Variables initialization
blocksize=1024
sampler = 44100
audio_buffer = []
out_dir = "out/"
temp_dir = "temp/"

# Draws to the canvas of time and freq domains the input data
def graph_audio_buffer(buff):
    # Updates time domain graph
    line_time.set_data(range(len(buff)), buff)
    ax_time.relim()
    ax_time.autoscale_view()
    canvas_time.draw()

    # Updates frequency domain graph
    window = np.hamming(len(buff))
    spectrum = np.abs(fftshift(fft(window * buff)))
    freqs = fftshift(fftfreq(len(buff), 1/sampler))
    line_freq.set_data(freqs, spectrum)
    ax_freq.relim()
    ax_freq.autoscale_view()
    canvas_freq.draw()

# Callback function used by the audio stream to generate the audio buffer
# Graphs in time and frequency domains
def record_callback(indata, frames, time, status):
    audio_buffer.extend(indata[:, 0])
    graph_audio_buffer(audio_buffer)

# Start a new recording
# If there is already one, stop it and calls save_atm_file
def start_recording():
    global audio_buffer

    # Stops or starts the recording
    if stream.active:
        record_button.configure(image=icon_mic)
        stream.stop()
        save_atm_file()
    else:
        record_button.configure(image=icon_stop)
        audio_buffer = []
        stream.start()

# Plays and graphs any audio buffered
def playback():
    sd.play(audio_buffer, sampler)
    graph_audio_buffer(audio_buffer)

# Runs on the audio thread to improve performance
def play_audio():
    sd.play(audio_buffer, sampler)

# Stores the audio buffer to an atm file on the out directory
def save_atm_file():
    now = datetime.datetime.now()
    date_string = now.strftime("%d%m%Y%H%M%S")
    np.save(out_dir+st.atm_output_file, audio_buffer)
    os.replace(out_dir+st.atm_output_file+".npy", out_dir+date_string+st.atm_output_file)

# Prompts the user to open a file and calls the load_audio function if one is selected
def open_file():
    filetypes = (
        ('autrum files', '*.atm'),
        ('All files', '*.*')
    )
    current_dir = os.getcwd()+out_dir
    selected_file_path = filedialog.askopenfilename(filetypes=filetypes, initialdir=current_dir)

    # Validates if a file was selected
    if selected_file_path:
        file_label.config(text=st.file_selected_label+selected_file_path)
        play_btn_state = tk.NORMAL
        load_audio()
    else:
        file_label.config(text=st.file_not_selected_label)
        play_btn_state = tk.DISABLED
    
    play_button.configure(state=play_btn_state)

# Process the atm file to load the data into the audio buffer
def load_audio():
    global audio_buffer
    audio_data = np.load(out_dir+st.atm_output_file, 'r')
    write(temp_dir+st.temp_audio_file, sampler, audio_data)
    audio_buffer = audio_data

    # Clears the graphs
    line_time.set_data([], [])
    line_freq.set_data([], [])
    canvas_time.draw()
    canvas_freq.draw()



# Set up button callbacks
record_button.configure(command=start_recording)
play_button.configure(command=playback)
open_button.configure(command=open_file)

# Initializes the audio input stream
stream = sd.InputStream(samplerate=sampler, blocksize=2048, channels=1, callback=record_callback)

# Starts the application
root.mainloop()
