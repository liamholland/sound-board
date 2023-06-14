import tkinter as tk
import pyaudio as pa
import os
import wave

#create and set up window
window = tk.Tk()
frame = tk.Frame()
frame.grid()

#function to refresh the application
def get_num_recordings():
    curr_dir = os.getcwd()  #get the current directory
    
    count = 0
    
    #count the number of .wav files in the directory
    for file in os.listdir(curr_dir):
        if os.path.isfile(os.path.join(curr_dir, file)) and file.endswith('.wav'):
            count += 1
        
    return count
#end of function refresh_interface

#function to record audio
def record_audio():
    #settings for recording
    CHUNK = 1024
    SAMPLE_FORMAT = pa.paInt16
    CHANNELS = 1
    FS = 44100
    SECONDS = 2
    FILENAME = f"recording{get_num_recordings() + 1}.wav"

    p = pa.PyAudio()    #initialise

    print("recording...")

    #open a stream with the settings
    stream = p.open(format=SAMPLE_FORMAT,
                    channels=CHANNELS,
                    rate=FS,
                    frames_per_buffer=CHUNK,
                    input=True)
    
    frames = []

    #record the data
    for _ in range(0, int(FS / CHUNK * SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    #close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()   

    print("...recording finished")

    #save the data to a file with the same settings
    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
    wf.setframerate(FS)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    add_buttons()
    return
#end of function record_audio

#function to retrieve the names of recording files
def get_recording_names():
    files = os.listdir(os.getcwd())
    recordings = []
    
    for file in files:
        if file.endswith('.wav'):
            recordings.append(file)
    
    return recordings
#end of function get_recording_names

#function to add buttons to the ui
def add_buttons():    
    #record and quit buttons buttons
    tk.Button(frame, text="Record", command=record_audio).grid(column=0, row=0)
    tk.Button(frame, text="Quit", command=window.destroy).grid(column=1, row=0)
    
    names = get_recording_names()
    
    for i in range(0, get_num_recordings()):
        tk.Button(frame, text=f"{names[i]}").grid(column=0, row=i+1)
    
    return
#end of function add_buttons

add_buttons()

window.mainloop()   #run program