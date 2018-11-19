import argparse
import time
import threading

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder
from FFT import Tracer_spectre

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')
        board.button.wait_for_press()
        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)
        record_file(AudioFormat.CD, filename=args.filename, wait=wait, filetype='wav')
    
        rate,data = wave.read("recoding.wav")    #Lit le son. Conserve les amplitudes dans la variable data
        n = data.size
        duree = 1.0*n/rate
        a = chain(*data)
        data2 = list(a)
        Tracer_spectre(0,.5,data2,rate)


if __name__ == '__main__':
    main()
