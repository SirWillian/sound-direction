from collections import deque
from typing import Deque, Tuple

from numpy import array, float32
from numpy.typing import NDArray


class SoundElement:
    position: NDArray[float32]
    samples: Deque[float]

    def __init__(self, sample_rate=44100):
        self.position = array([0.0, 0.0, 0.0])
        self.samples = deque()
        self.sample_rate = sample_rate

    def add_sample(self, sample):
        # TODO: Add a limit to sample sound at some point
        self.samples.append(sample)

    def get_sample_count(self):
        return len(self.samples)
