import argparse
import time
import wave,struct
import threading
import math
from numpy.fft import fft, rfftfreq
import argparse
import sounddevice
from itertools import chain

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def determine_note_fondamentale():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')
        board.button.wait_for_press()
        done = threading.Event()
        board.button.when_pressed = done.set

        fs = 60000
        duration = 2 # seconds
        myrecording = sounddevice.rec(int(duration * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        print("done recording")
        myrecording2 = list(chain(*myrecording))
        

        """def readwave(filename):
            wav = wave.open(filename)
            nchannels = wav.getnchannels()
            nframes = wav.getnframes()
            sampwidth = wav.getsampwidth()
            framerate = wav.getframerate()
            frames = wav.readframes(nframes)

            if sampwidth == 1:
                # 8 bit : unsigned char
                data = struct.unpack('%sB' % (nframes * nchannels), frames)

            elif sampwidth == 2:
                # 16 bits : signed short
	            data = struct.unpack('%sh' % (nframes * nchannels), frames)
            return (data,framerate)

        recording_name = '../AIY-projects-python/src/examples/voice/recording.wav'"""
        data = myrecording2

        rate = fs


        start = int(0*rate)
        stop = int((0+1)*rate)
        spectre = fft(data[start:stop])
        n = spectre.size
        timestep = 1/60000
        freq = rfftfreq(n, d=timestep)
	

        print(freq)
        return(freq[1])

if __name__=='__main__':
    determine_note_fondamentale()

