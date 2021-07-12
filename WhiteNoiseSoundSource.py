import numpy as np
from GeneratorSoundSource import GeneratorSoundSource


class WhiteNoiseSoundSource(GeneratorSoundSource):
    def __init__(self, sample_rate, amplitude=1):
        self.amplitude = amplitude

        def generator_function(x):
            return self.amplitude * np.random.random_sample()
        super().__init__(sample_rate, generator_function=generator_function)
