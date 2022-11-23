import itertools
import os
import sys
import time
from math import cos, radians, sin, sqrt
from typing import List

from test_utils import create_test_writer, get_test_name, save_wav_samples

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))

from Microphone import Microphone
from SineWaveSoundSource import SineWaveSoundSource
from SoundDirectionDetector import SoundDirectionDetector
from SoundEnvironment import SoundEnvironment

test_name = get_test_name(__file__)
outfile, csvwriter = create_test_writer(test_name)
csvwriter.writerow(["mic_shape", "shape_side", "sound_amplitude", "sound_freq", "sound_dist", "sound_dir", "detected_dir", "detection_error", "sim_time", "detection_time"])

## Environment initialization
sample_rate = 44100 # sampling rate, Hz, must be integer
amplitude = 0.1
sim_duration = 3.0  # in seconds, may be float
source_dist = 5  # meters
#source_dirs = [45, 46, 47, 48, 49, 50, 51, 52, 53]
source_dirs = list(range(180, -180, -10))

## Source setup
# Pure wave sources
sources: List[SineWaveSoundSource]
sources = []
#frequencies = [100, 500, 1000, 2000, 5000, 10000]
frequencies = [1000]
for f in frequencies:
    sources.append(SineWaveSoundSource(sample_rate, amplitude, f))

# Test for each frequency and direction
for source, dir in itertools.product(sources, source_dirs):
    print(''); print(f'{repr(source)} {source_dist}m {dir}deg')

    # Microphone setup (equilateral, 10cm side, no noise)
    mic_tri_side = 0.1
    mic1 = Microphone(sample_rate)
    mic1.position[0]=mic_tri_side/2
    mic2 = Microphone(sample_rate)
    mic2.position[0]=-mic_tri_side/2
    mic3 = Microphone(sample_rate)
    mic3.position[1]=mic_tri_side*sqrt(3)/2
    #mic4 = Microphone(sample_rate)

    ## Detector setup
    # Add microphone array to the detector
    detector = SoundDirectionDetector(sample_rate, sample_time_window=1.0)
    detector.add_microphone(mic2)
    detector.add_microphone(mic1)
    detector.add_microphone(mic3)

    # Add sources and microphones to the simulation environment and run simulation
    source.position[0] = source_dist * cos(radians(dir))
    source.position[1] = source_dist * sin(radians(dir))
    env = SoundEnvironment(sample_rate, int(sim_duration*sample_rate))
    env.add_microphone(mic1)
    env.add_microphone(mic2)
    env.add_microphone(mic3)
    env.add_source(source)

    sim_start = time.time()
    env.run_simulation()
    sim_end = time.time()
    sim_real_time = sim_end - sim_start
    print("real time spent simulating:", sim_real_time)

    # Detect sound direction
    detection_start = time.time()
    direction = detector.detect_sound_direction()
    detection_end = time.time()
    detection_time = detection_end - detection_start
    print('sound direction:', direction, "detection time", detection_time)
    csvwriter.writerow(["equi", mic_tri_side, amplitude, source.frequency, source_dist, dir, direction, abs(dir-direction), sim_real_time, detection_time])
    save_wav_samples(mic1.samples, sample_rate, str(source.frequency)+"Hz", test_name, str(dir))

outfile.close()