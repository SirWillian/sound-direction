import math

from Microphone import Microphone
from SoundSource import SoundSource


class NoisyMicrophone(Microphone):
    noise_source: SoundSource
    "Sound source to be used as noise on every sample added"
    snr: float
    "Signal-to-noise ratio"
    snr_window: float
    "Time window (in seconds) of last samples to consider when computing SNR"

    def __init__(self, noise_source: SoundSource, sample_rate=44100, snr = 20, snr_window = 0.125):
        self.noise_source = noise_source
        self.original_samples = list()
        self.noise_samples = list()
        self.snr = snr
        self.snr_window = snr_window
        self.__pending_samples = 0
        self.__original_mean_squared = 0 # RMS, but without the square root
        self.__noise_mean_squared = 0 # RMS, but without the square root
        super().__init__(sample_rate)

    def add_sample(self, sample):
        sample_window = int(self.snr_window * self.sample_rate)
        if (self.__pending_samples < sample_window):
            noise = self.noise_source.emit_sound()
            self.original_samples.append(sample)
            self.noise_samples.append(noise)
            self.__original_mean_squared += sample**2/sample_window
            self.__noise_mean_squared += noise**2/sample_window
            self.__pending_samples += 1
        else:
            # Modulate noise's amplitude to meet the desired noise RMS
            # Calculate the ratio between the generated noise RMS and the target value
            # Apply that ratio to the appropriate noise sample
            noise = self.noise_source.emit_sound()
            pending_noise = self.noise_samples[-sample_window]
            target_noise_ms = self.__original_mean_squared/(10**(self.snr/10))
            #if (len(self.original_samples) > 94000):
            #    print(self.__original_mean_squared, noise_ms, self.__noise_mean_squared, sample, self.original_samples[-sample_window])
            noise_ratio = math.sqrt(target_noise_ms / self.__noise_mean_squared)
            #try:
            #except ValueError:
            #    print(self.__original_mean_squared, noise_ms, self.__noise_mean_squared)
            final_noise = pending_noise * noise_ratio
            self.noise_samples[-sample_window] = final_noise
            # Update mean squared values of the sample window
            pending_sample = self.original_samples[-sample_window]
            self.__original_mean_squared += (sample**2 - pending_sample**2)/sample_window
            self.__noise_mean_squared += (noise**2 - pending_noise**2)/sample_window
            # Cummulative floating point errors may cause these members to go below 0
            # Just reset the MS values if that happens
            if (self.__original_mean_squared < 0.0): self.__original_mean_squared = 0
            if (self.__noise_mean_squared < 0.0): self.__noise_mean_squared = 0
            # Save samples on their respective lists
            # Save them after the operations above to simplify indexing the lists
            final_sample = pending_sample + final_noise
            self.original_samples.append(sample)
            self.noise_samples.append(noise)
            super().add_sample(final_sample)

    def calc_pending_noise(self):
        target_noise_ms = self.__original_mean_squared/(10**(self.snr/10))
        noise_ratio = math.sqrt(target_noise_ms / self.__noise_mean_squared)
        for i in range(self.__pending_samples):
            noise = self.noise_samples[-self.__pending_samples+i] * noise_ratio
            self.noise_samples[-self.__pending_samples+i] = noise
            super().add_sample(self.original_samples[-self.__pending_samples+i]+noise)
        self.__pending_samples = 0

    def post_simulation(self):
        self.calc_pending_noise()
