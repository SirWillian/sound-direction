from SoundElement import SoundElement


class SoundSource(SoundElement):
    def __init__(self, sample_rate=44100):
        super().__init__(sample_rate)

    def emit_sound(self):
        return self.samples.popleft()
