import numpy as np

from GeneratorSoundSource import GeneratorSoundSource


class SineWaveSoundSource(GeneratorSoundSource):
    def __init__(self, sample_rate, amplitude, frequency, phase_delay=0.0):
        self.amplitude = amplitude
        self.frequency = frequency
        # TODO: fazer delay usando tempo e não radianos
        self.phase_delay = phase_delay

        def generator_function(x):
            return np.float32(self.amplitude*np.sin(2*np.pi * self.frequency * x / self.sample_rate + self.phase_delay))
        super().__init__(sample_rate, generator_function=generator_function)

    def __repr__(self) -> str:
        return 'SineWaveSoundSource(' + str(self.sample_rate) + ',' + str(self.amplitude) + ',' + str(self.frequency) + ',' + str(self.phase_delay) + ')'
