from SoundElement import SoundElement


class SoundSource(SoundElement):
    def __init__(self, sample_rate=44100):
        super().__init__(sample_rate)

    def emit_sound(self):
        # If we run out of samples, emit 0.0
        try:
            return self.samples.popleft()
        except IndexError:
            return 0.0
