import numpy as np
from GeneratorSoundSource import GeneratorSoundSource


class SineWaveSoundSource(GeneratorSoundSource):
    def __init__(self, sample_rate, amplitude, frequency, phase_delay=0.0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_delay = phase_delay

        def generator_function(x):
            # TODO: For an array, i'd use .astype(np.float32). Not sure how to enforce that for a single sound
            return self.amplitude*np.sin(2*np.pi *
                                         self.frequency*x/self.sample_rate + self.phase_delay)
        super().__init__(sample_rate, generator_function=generator_function)
