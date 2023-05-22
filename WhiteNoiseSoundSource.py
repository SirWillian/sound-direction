import numpy as np
from GeneratorSoundSource import GeneratorSoundSource


class WhiteNoiseSoundSource(GeneratorSoundSource):
    def __init__(self, sample_rate, amplitude=1.0):
        self.amplitude = amplitude

        def generator_function(x):
            return self.amplitude * (2 * np.random.random_sample() - 1)
        super().__init__(sample_rate, generator_function=generator_function)
