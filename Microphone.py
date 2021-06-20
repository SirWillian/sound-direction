from SoundElement import SoundElement

class Microphone(SoundElement):
    def __init__(self, sample_rate=44100):
        super().__init__(sample_rate)

    