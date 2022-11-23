import itertools
import os
import sys
import time
from math import cos, radians, sin, sqrt

from test_utils import (create_test_writer, get_test_name, load_sample,
                        save_wav_samples)

project_root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
if __name__ == '__main__':
    sys.path.insert(0, project_root_path)

from Microphone import Microphone
from SoundDirectionDetector import SoundDirectionDetector
from SoundEnvironment import SoundEnvironment
from WavFileSoundSource import WavFileSoundSource

test_name = get_test_name(__file__)
outfile, csvwriter = create_test_writer(test_name)
csvwriter.writerow(["mic_shape", "shape_side", "sound_amplitude", "sample_name", "sound_dist", "sound_dir", "detected_dir", "detection_error", "sim_time", "detection_time"])

## Environment initialization
sample_rate = 44100 # sampling rate, Hz, must be integer
amplitude = 0.1
sim_duration = 3.0  # in seconds, may be float
source_dist = 5  # meters
source_dirs = [45, 46, 47, 48, 49, 50, 51, 52, 53]

## Source setup
# Sample sources
sample_names = ["branches-10khz", "glass-10khz", "gymball-10khz"]

# Test for each sample and direction
for sample_name, dir in itertools.product(sample_names, source_dirs):
    # Reload sample every test
    source = load_sample(sample_name)
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
    detector = SoundDirectionDetector(sample_rate, sample_time_window=1.5)
    detector.add_microphone(mic2)
    detector.add_microphone(mic1)
    detector.add_microphone(mic3)

    # Add sources and microphones to the simulation environment and run simulation
    source.position[0] = source_dist * cos(radians(dir))
    source.position[1] = source_dist * sin(radians(dir))
    env = SoundEnvironment(sample_rate, min(len(source.samples), int(sim_duration*sample_rate)))
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
    csvwriter.writerow(["equi", mic_tri_side, amplitude, os.path.basename(source.filepath), source_dist, dir, direction, abs(dir-direction), sim_real_time, detection_time])
    save_wav_samples(mic1.samples, sample_rate, sample_name, test_name, "mic1")

outfile.close()
