import tkinter as tk
import pyaudio as pa
import wave

ready = False

#function to record audio
def record_audio():
    print("Function called")
    if ready == True:
        CHUNK = 1024
        SAMPLE_FORMAT = pa.paInt16
        CHANNELS = 1
        FS = 44100
        SECONDS = 3
        FILENAME = "recording.wav"

        p = pa.PyAudio()

        print("recording...")

        stream = p.open(format=SAMPLE_FORMAT,
                        channels=CHANNELS,
                        rate=FS,
                        frames_per_buffer=CHUNK,
                        input=True)
        
        frames = []

        for i in range(0, int(FS / CHUNK * SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        p.terminate()

        print("...recording finished")

        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FS)
        wf.writeframes(b''.join(frames))
        wf.close()
#end of function record_audio

#create and set up window
window = tk.Tk()
frame = tk.Frame()
frame.grid()

#add elements
tk.Button(frame, text="Record", command=record_audio).grid(column=0, row=0)   #record button
tk.Button(frame, text="Quit", command=window.destroy).grid(column=0, row=1) #quit button

ready = True
window.mainloop()   #run program


    
