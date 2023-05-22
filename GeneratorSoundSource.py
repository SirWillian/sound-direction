from typing import Callable
from SoundSource import SoundSource


class GeneratorSoundSource(SoundSource):
    __sounds_emitted: int
    __generator_function: Callable[[int], float]

    def __init__(self, sample_rate: int, generator_function: Callable[[int], float]=None):
        super().__init__(sample_rate=sample_rate)
        self.__generator_function = generator_function
        self.__sounds_emitted = 0

    def emit_sound(self):
        if not callable(self.__generator_function):
            return 0.0
        return_value = self.__generator_function(self.__sounds_emitted)
        self.__sounds_emitted += 1
        return return_value

    def get_sample_count(self):
        return -1