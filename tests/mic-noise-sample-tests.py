import itertools
import math
import os
import sys
import time
from math import cos, radians, sin, sqrt
from typing import List, Tuple

from test_utils import (create_test_writer, get_test_name, load_sample,
                        save_wav_samples)

project_root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
if __name__ == '__main__':
    sys.path.insert(0, project_root_path)

from Microphone import Microphone
from NoisyMicrophone import NoisyMicrophone
from PowerLawNoiseSoundSource import PowerLawNoiseSoundSource
from SoundDirectionDetector import SoundDirectionDetector
from SoundEnvironment import SoundEnvironment
from SoundSource import SoundSource
from WavFileSoundSource import WavFileSoundSource
from WhiteNoiseSoundSource import WhiteNoiseSoundSource

#outfile = open(os.path.splitext(__file__)[0]+'.csv', 'w', newline='')
#csvwriter = csv.writer(outfile)
test_name = get_test_name(__file__)
outfile, csvwriter = create_test_writer(test_name)
csvwriter.writerow(["mic_shape", "shape_side", "sound_amplitude", "noise_snr", "noise_type", "sample_name", "sound_dist", "sound_dir", "detected_dir", "detection_error", "sim_time", "detection_time"])

## Environment initialization
sample_rate = 44100 # sampling rate, Hz, must be integer
decay_rate = 0.5
sim_duration = 3.0  # in seconds, may be float
source_dist = 5  # meters
#source_dirs = [45, 46, 47, 48, 49, 50, 51, 52, 53]
source_dirs = [47]
#source_dirs = list(range(180, -180, -10))

## Source and noise setup
sample_names = ["branches-10khz", "glass-10khz", "gymball-10khz"]
source_noise_pairs: List[Tuple[float, str, str, float, SoundSource]]
source_noise_pairs = []
for name in sample_names:
    src = load_sample(name)
    for snr in [-20, 0, 20, 40, 60]: #snr in db
        # calculate decay on so the noise is created accordingly
        amplitude = abs(max(src.samples, key=abs))
        expected_signal = amplitude * (math.e ** (-decay_rate * source_dist))
        noise_amplitude = math.sqrt(expected_signal**2/(10**(snr/20)))
        print(f'{os.path.basename(src.filepath)} {snr} src amp {amplitude} expected signal {expected_signal} noise amp {noise_amplitude}')
        source_noise_pairs.append((snr, "white", name, amplitude, WhiteNoiseSoundSource(sample_rate, noise_amplitude)))
        source_noise_pairs.append((snr, "pink", name, amplitude, PowerLawNoiseSoundSource(sample_rate, 1, noise_amplitude)))

# Test for each sample, noise source and direction
# Repeating 4 times to accomodate for noise randomness
for sound_noise, dir in itertools.product(source_noise_pairs, source_dirs):
    for i in range(4):
        snr, noise_type, sample_name, src_amplitude, noise_source = sound_noise # unpack tuple
        # Reload sample every test
        sound_source = load_sample(sample_name)
        print(''); print(f'{repr(sound_source)} attempt {i} {source_dist}m {noise_type} noise {snr}dB {dir}deg')

        # Microphone setup (equilateral, 10cm side, no noise)
        mic_tri_side = 0.1
        mic1 = NoisyMicrophone(noise_source, sample_rate)
        mic1.position[0]=mic_tri_side/2
        mic2 = NoisyMicrophone(noise_source, sample_rate)
        mic2.position[0]=-mic_tri_side/2
        mic3 = NoisyMicrophone(noise_source, sample_rate)
        mic3.position[1]=mic_tri_side*sqrt(3)/2
        #mic4 = Microphone(sample_rate)

        ## Detector setup
        # Add microphone array to the detector
        detector = SoundDirectionDetector(sample_rate, sample_time_window=1.5)
        detector.add_microphone(mic2)
        detector.add_microphone(mic1)
        detector.add_microphone(mic3)

        # Add sources and microphones to the simulation environment and run simulation
        sound_source.position[0] = source_dist * cos(radians(dir))
        sound_source.position[1] = source_dist * sin(radians(dir))
        env = SoundEnvironment(sample_rate, int(sim_duration*sample_rate), decay_rate=decay_rate)
        env.add_microphone(mic1)
        env.add_microphone(mic2)
        env.add_microphone(mic3)
        env.add_source(sound_source)

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
        csvwriter.writerow(["equi", mic_tri_side, src_amplitude, snr, noise_type, os.path.basename(sound_source.filepath), source_dist, dir, direction, abs(dir-direction), sim_real_time, detection_time])
        save_wav_samples(mic1.samples, sample_rate, sample_name, test_name, str(snr), noise_type, "combined")
        save_wav_samples(mic1.original_samples, sample_rate, sample_name, test_name, str(snr), noise_type, "original")
        save_wav_samples(mic1.noise_samples, sample_rate, sample_name, test_name, str(snr), noise_type, "noise")

outfile.close()
