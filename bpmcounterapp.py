from flask import Flask, render_template, jsonify
import threading
import pyaudio
import numpy as np
import librosa

app = Flask(__name__)

RECORD_SECONDS = 5
sampleRate = 44100

# 결과를 저장할 전역 변수
result_tempo = 0


def record_and_track():
    global result_tempo
    while True:
        p = pyaudio.PyAudio()

        chunk = int(sampleRate * RECORD_SECONDS)

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=sampleRate,
                        input=True,
                        frames_per_buffer=chunk)

        sound = stream.read(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

        np_sound = np.frombuffer(sound, dtype=np.float32)
        tempo, beat_frames = librosa.beat.beat_track(y=np_sound, sr=sampleRate)
        result_tempo = round(tempo)
        print(f'Tempo: {result_tempo} BPM')


thread = threading.Thread(target=record_and_track)
thread.start()


@app.route('/get_tempo')
def get_tempo():
    global result_tempo
    return jsonify(tempo=result_tempo)


@app.route('/')
def home():
    return render_template('index.html', tempo=result_tempo)


if __name__ == '__main__':
    app.run()
