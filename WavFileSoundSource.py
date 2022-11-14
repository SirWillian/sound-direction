from collections import deque

import numpy as np
from scipy.io import wavfile

from SoundSource import SoundSource


class WavFileSoundSource(SoundSource):
    def __init__(self, filepath, volume_factor=1.0):
        self.__filepath = filepath
        #TODO: interp sample rate to the desired sample rate
        sample_rate, samples = wavfile.read(filepath)
        super().__init__(sample_rate=sample_rate)
        # figure out the input range to remap to the [-1,1] range (if needed)
        # take the mean between the channels to convert from stereo to mono
        if (samples.dtype == np.float32):
            self.samples = deque([np.mean(sample)*volume_factor for sample in samples])
        else:
            # precompute range remapping factor (new range / old range)
            # this will turn signed integer zeros into non-zero floats because the negative range is bigger
            # than the positive range. we could add 1 to the old range to account for zero (counting how
            # many numbers the old range has), but that leads to never being able to reach the new range max
            remap_factor = (2.0/(np.iinfo(samples.dtype).max - np.iinfo(samples.dtype).min))
            input_range_min = np.iinfo(samples.dtype).min
            self.samples = deque(
                [(((np.mean(sample)-input_range_min)*remap_factor) - 1.0)*volume_factor for sample in samples])

    @property
    def filepath(self):
        return self.__filepath

    def __repr__(self) -> str:
        return 'WavFileSoundSource(' + self.__filepath + ')'
