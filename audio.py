import pyaudio
import wave


# Configuration
FORMAT = pyaudio.paInt16 #Audio format (16-bit)
CHANNELS = 1 # Mono audio
RATE = 44100 # SAMPLE RATE (samples per second)
CHUNK = 1024 # Buffer size (frames per buffer)
RECORD_SECONDS = 10 # Duration of recording
OUTPUT_FILENAME = "recorded_audio.wav"


audio = pyaudio.PyAudio()

stream = audio.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)

print("recording.....")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow = False)
    frames.append(data)

print("FINISHED RECORDING >>>>>>")

stream.stop_stream()
stream.close()
audio.terminate()


#Save the recorded data as a wav file
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f'Audio saved to {OUTPUT_FILENAME}')



