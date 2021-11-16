import math
from collections import namedtuple
from typing import Dict, List

import numpy as np

from Microphone import Microphone
from SoundSource import SoundSource


class SoundEnvironment:
    sources: List[SoundSource]
    microphones: List[Microphone]

    def __init__(self, sample_rate=44100, max_samples=-1, speed_of_sound = 343, decay_rate = 0.5) -> None:
        self.sources = []
        self.microphones = []
        self.sample_rate = sample_rate
        self.simulated_samples = 0
        self.max_samples = max_samples
        self.speed_of_sound = speed_of_sound
        self.decay_rate = decay_rate

    def add_source(self, source: SoundSource) -> None:
        self.sources.append(source)

    def add_microphone(self, microphone: Microphone) -> None:
        self.microphones.append(microphone)

    def run_simulation(self) -> None:
        # How many samples are we simulating?
        # Up to the minimum between max_samples and the highest sample count among all sources
        samples_to_simulate = self.max_samples
        source_sample_counts = [source.get_sample_count() for source in self.sources]
        if len(source_sample_counts) != 0 and samples_to_simulate == -1:
            samples_to_simulate = max(source_sample_counts)
        # If no sources have a limit and max_samples wasn't set, don't simulate
        if samples_to_simulate == -1:
            return

        # Construct a queue for the sounds emitted by sources and when they should hit each microphone
        SampleListElement = namedtuple('SampleListElement', ['value', 'time'])
        emitted_sample_list: Dict[Microphone, List[SampleListElement]]
        emitted_sample_list = {m: list() for m in self.microphones}

        # Delay (number of samples rounded up) will be a function of the distance between the source and the microphone
        def calculate_delay(source: SoundSource, microphone: Microphone):
            return math.ceil((np.linalg.norm(source.position - microphone.position) / self.speed_of_sound) * self.sample_rate)

        # Exponential decay
        def apply_decay(sample, source, microphone):
            return sample * (math.e ** (-self.decay_rate * np.linalg.norm(source.position - microphone.position)))

        # Start simulating
        while self.simulated_samples != samples_to_simulate:
            # if self.simulated_samples % 100 == 0:
            #     print(self.simulated_samples)
            # Emit a sample for each source and queue their arrival on each microphone
            for source in self.sources:
                source_sample = source.emit_sound()
                #print(source_sample)
                for mic in self.microphones:
                    decayed_sample = apply_decay(source_sample, source, mic)
                    sample_toa = self.simulated_samples + calculate_delay(source, mic)
                    #print(decayed_sample, sample_toa)
                    emitted_sample_list[mic].append(SampleListElement(decayed_sample, sample_toa))

            # Check which samples should arrive at the microphone now
            for mic in self.microphones:
                # Sum all samples that are supposed to arrive at this microphone at this time
                arriving_samples = [sle for sle in emitted_sample_list[mic]
                                    if sle.time == self.simulated_samples]
                # TODO: figure out correct way of adding samples together
                combined_samples = sum(map(lambda x: x.value, arriving_samples))
                # Clip value to the [-1, 1] range
                # TODO: test with and without clipping
                combined_samples = min(max(combined_samples, -1.0), 1.0)
                mic.add_sample(combined_samples)
                # Clean list
                for sample in arriving_samples:
                    emitted_sample_list[mic].remove(sample)
            self.simulated_samples += 1
