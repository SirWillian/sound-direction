from collections import deque
from Microphone import Microphone
from SoundSource import SoundSource


class NoisyMicrophone(Microphone):
    noise_source: SoundSource
    "Sound source to be used as noise on every sample added"
    snr: float
    "Signal-to-noise ratio"

    def __init__(self, noise_source: SoundSource, sample_rate=44100):
        self.noise_source = noise_source
        self.original_samples = deque()
        self.noise_samples = deque()
        super().__init__(sample_rate)

    def add_sample(self, sample):
        noise = self.noise_source.emit_sound()
        final_sample: float
        # TODO: SNR is more of a thing across a range of samples, like some average
        # doing it on a sample by sample basis may not be correct
        """
        if (self.snr >= 1):
            # if SNR was 1, noise would be the same intensity as the sample
            # noise is somewhere between [-1,1], so multiplying it by the abs value of the sample
            # will ensure that ratio
            rescaled_noise = noise * abs(sample)
            final_sample = sample * (self.snr / (self.snr + 1)) + rescaled_noise / (self.snr + 1)
        else:
            rescaled_sample = sample * abs(noise)
            nsr = 1/self.snr
            final_sample = noise * (nsr / (nsr + 1)) + rescaled_sample / (nsr + 1)
        #print(sample, noise, final_sample)
        """
        self.original_samples.append(sample)
        self.noise_samples.append(noise)
        final_sample = sample + noise
        super().add_sample(final_sample)
