import itertools
import math
import os
import sys
import time
from math import cos, radians, sin, sqrt

from test_utils import (create_test_writer, get_test_name, load_sample,
                        save_wav_samples)

project_root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
if __name__ == '__main__':
    sys.path.insert(0, project_root_path)

from NoisyMicrophone import NoisyMicrophone
from SineWaveSoundSource import SineWaveSoundSource
from SoundDirectionDetector import SoundDirectionDetector
from SoundEnvironment import SoundEnvironment
from WhiteNoiseSoundSource import WhiteNoiseSoundSource

test_name = get_test_name(__file__)
outfile, csvwriter = create_test_writer(test_name)
csvwriter.writerow(["mic_shape", "shape_side", "sound_amplitude", "noise_snr", "noise_type","sound_name", "sound_dist", "detection_window", "sound_dir", "detected_dir", "detection_error", "sim_time", "detection_time"])

## Environment initialization
sample_rate = 44100 # sampling rate, Hz, must be integer
decay_rate = 0.5
sim_duration = 3.0  # in seconds, may be float
source_dist = 5  # meters
source_dir = 30 # degrees
amplitude = 0.1
snr = 20
detection_windows = [0.1, 0.25, 0.5, 1.0, 1.5] # seconds

## Source setup
sources = [("pure", "1000Hz"),("sample", "glass-10khz"),("sample", "branches-10khz"),("sample", "gymball-10khz")]
#sources = [("sample", "gymball-10khz")]

# Test for each source and direction
for src, detection_window in itertools.product(sources, detection_windows):
    src_type, sound_name = src # unpack tuple
    for i in range(4):
        # Reload source every test
        if src_type == "pure":
            freq = int(sound_name[:-2])
            src_amplitude = amplitude
            sound_source = SineWaveSoundSource(sample_rate, src_amplitude, freq)
            sim_samples = int(sim_duration*sample_rate)
        else:
            sound_source = load_sample(sound_name)
            src_amplitude = abs(max(sound_source.samples, key=abs))
            sim_samples = len(sound_source.samples)
        #expected_signal = src_amplitude * (math.e ** (-decay_rate * source_dist))
        #noise_amplitude = math.sqrt(expected_signal**2/(10**(snr/20)))
        print(''); print(f'{repr(sound_source)} attempt {i} {source_dist}m white noise {snr}dB {source_dir}deg {detection_window}s window')

        # Microphone setup (equilateral, 10cm side, no noise)
        mic_tri_side = 0.1
        mic1 = NoisyMicrophone(WhiteNoiseSoundSource(sample_rate), sample_rate, snr)
        mic1.position[0]=mic_tri_side/2
        mic2 = NoisyMicrophone(WhiteNoiseSoundSource(sample_rate), sample_rate, snr)
        mic2.position[0]=-mic_tri_side/2
        mic3 = NoisyMicrophone(WhiteNoiseSoundSource(sample_rate), sample_rate, snr)
        mic3.position[1]=mic_tri_side*sqrt(3)/2
        #mic4 = Microphone(sample_rate)

        ## Detector setup
        # Add microphone array to the detector
        detector = SoundDirectionDetector(sample_rate, sample_time_window=detection_window)
        detector.add_microphone(mic2)
        detector.add_microphone(mic1)
        detector.add_microphone(mic3)

        # Add sources and microphones to the simulation environment and run simulation
        sound_source.position[0] = source_dist * cos(radians(source_dir))
        sound_source.position[1] = source_dist * sin(radians(source_dir))
        env = SoundEnvironment(sample_rate, sim_samples, decay_rate=decay_rate)
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
        csvwriter.writerow(["equi", mic_tri_side, src_amplitude, snr, "white", sound_name, source_dist, detection_window, source_dir, direction, abs(source_dir-direction), sim_real_time, detection_time])
        save_wav_samples(mic1.samples, sample_rate, sound_name, test_name, str(detection_window), "combined")
        save_wav_samples(mic1.noise_samples, sample_rate, sound_name, test_name, str(detection_window), "noise")
        save_wav_samples(mic1.original_samples, sample_rate, sound_name, test_name, str(detection_window), "original")

outfile.close()
