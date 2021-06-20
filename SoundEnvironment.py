from collections import namedtuple
from typing import Dict, List

from Microphone import Microphone
from SoundSource import SoundSource


class SoundEnvironment:
    sources: List[SoundSource]
    microphones: List[Microphone]

    def __init__(self, sample_rate=44100, max_samples=-1) -> None:
        self.sources = []
        self.microphones = []
        self.sample_rate = sample_rate
        self.simulated_samples = 0
        self.max_samples = max_samples

    def add_source(self, source: SoundSource) -> None:
        self.sources.append(source)

    def add_microphone(self, microphone: Microphone) -> None:
        self.microphones.append(microphone)

    def run_simulation(self) -> None:
        # How many samples are we simulating?
        # Up to the minimum between max_samples and the lowest sample count among all sources
        # If no sources have a limit and max_samples wasn't set, simulate indefinitely
        # TODO: implement max_samples check
        samples_to_simulate = -1
        source_sample_counts = [source.get_sample_count()
                                for source in self.sources if source.get_sample_count != -1]
        if len(source_sample_counts) != 0:
            samples_to_simulate = min(source_sample_counts)

        # Construct a queue for the sounds emitted by sources and when they should hit each microphone
        SampleListElement = namedtuple('SampleListElement', ['value', 'time'])
        emitted_sample_list: Dict[Microphone, List[SampleListElement]]
        emitted_sample_list = {m: list() for m in self.microphones}

        # Delay will be a function of the distance between the source and the microphone
        def calculate_delay(source, microphone):
            return 0

        # No decay yet
        def apply_decay(sample, source, microphone):
            return sample

        # Start simulating
        while self.simulated_samples != samples_to_simulate:
            # Emit a sample for each source and queue their arrival on each microphone
            for source in self.sources:
                source_sample = source.emit_sound()
                for mic in self.microphones:
                    decayed_sample = apply_decay(source_sample, source, mic)
                    sample_toa = self.simulated_samples + calculate_delay(source, mic)
                    emitted_sample_list[mic].append(SampleListElement(decayed_sample, sample_toa))

            # Check which samples should arrive at the microphone now
            for mic in self.microphones:
                # Sum all samples that are supposed to arrive at this microphone at this time
                arriving_samples = [sle for sle in emitted_sample_list[mic]
                                    if sle.time == self.simulated_samples]
                # TODO: figure out correct way of adding samples together
                combined_samples = sum(map(lambda x: x.value, arriving_samples))
                # Clip value to the [-1, 1] range
                combined_samples = min(max(combined_samples, -1.0), 1.0)
                mic.add_sample(combined_samples)
                # Clean list
                for sample in arriving_samples:
                    emitted_sample_list[mic].remove(sample)
            self.simulated_samples += 1
