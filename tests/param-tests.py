import os
import sys
import time
from math import cos, radians, sin, sqrt

project_root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
if __name__ == '__main__':
    sys.path.insert(0, project_root_path)

from Microphone import Microphone
from NoisyMicrophone import NoisyMicrophone
from PowerLawNoiseSoundSource import PowerLawNoiseSoundSource
from SoundDirectionDetector import SoundDirectionDetector
from SoundEnvironment import SoundEnvironment
from WavFileSoundSource import WavFileSoundSource
from WhiteNoiseSoundSource import WhiteNoiseSoundSource

## Environment initialization
sample_rate = 44100 # sampling rate, Hz, must be integer
sim_duration = 2.0  # in seconds, may be float
env = SoundEnvironment(sample_rate, int(sim_duration*sample_rate))

## Source setup
source = WavFileSoundSource(os.path.join(project_root_path, "samples", "gymball.wav"))
source_dist = 50
source_dir = 53
source.position[0] = source_dist * cos(radians(53))
source.position[1] = source_dist * sin(radians(53))

# Microphone (and noise) setup
noise_source = WhiteNoiseSoundSource(sample_rate, 0.0)
#noise_source = PowerLawNoiseSoundSource(sample_rate, -1, volume)

# mic1 = NoisyMicrophone(noise_source, sample_rate)
# mic1.position[0]=-0.1/2
# mic2 = NoisyMicrophone(noise_source, sample_rate)
# mic2.position[0]=0.1/2
# #mic2.position[1]=0.03
# mic3 = NoisyMicrophone(noise_source, sample_rate)
# #mic3.position[1]=0.03
# mic4 = NoisyMicrophone(noise_source, sample_rate)
# mic4.position[1]=0.1*sqrt(3)/2

# Microphone setup (equilateral, 10cm side, no noise)
mic_tri_side = 0.1
mic1 = Microphone(sample_rate)
mic1.position[0]=mic_tri_side/2
mic2 = Microphone(sample_rate)
mic2.position[0]=-mic_tri_side/2
mic4 = Microphone(sample_rate)
mic4.position[1]=mic_tri_side*sqrt(3)/2

## Detector setup
# Add microphone array to the detector
#detector = SoundDirectionDetector(sample_rate, sample_count=132300)
detector = SoundDirectionDetector(sample_rate, sample_time_window=1.5)
#detector.add_microphone(mic3)
detector.add_microphone(mic2)
detector.add_microphone(mic1)
detector.add_microphone(mic4)

# Add sources and microphones to the simulation environment and run simulation
env.add_microphone(mic1)
env.add_microphone(mic2)
#env.add_microphone(mic3)
env.add_microphone(mic4)
env.add_source(source)

start = time.time()
env.run_simulation()
end = time.time()

# Detect sound direction
print("real time spent simulating:", end-start)
start = time.time()
direction = detector.detect_sound_direction()
end = time.time()

print('sound direction:', direction, "detection time", end-start)
