from collections import deque
from typing import Deque

import numpy as np
from sklearn.preprocessing import minmax_scale

from GeneratorSoundSource import GeneratorSoundSource

# Inspiration taken from:
# https://www.socsci.ru.nl/wilberth/python/noise.html
# https://stackoverflow.com/a/67127726


class PowerLawNoiseSoundSource(GeneratorSoundSource):
    # Generating samples requires an FFT and that only makes sense to do over multiple samples
    # Keep an internal buffer so a large chunk of samples can be pre-generated at a time
    __sample_buffer: Deque[float]

    def __init__(self, sample_rate, beta=1, amplitude=1):
        self.amplitude = amplitude
        self.beta = beta
        self.__sample_buffer = deque()

        # Alternate implementation. Seems a bit more chaotic
        # def spectrum_noise(N, psd=lambda f: 1):
        #    X_white = np.fft.rfft(np.random.randn(N))
        #    S = psd(np.fft.rfftfreq(N))
        #    S = S / np.sqrt(np.mean(S**2))
        #    X_shaped = X_white * S
        #    return np.fft.irfft(X_shaped)

        def pre_generate_samples():
            # real-fft frequencies (not the negative ones)
            # using sample_rate as the window length to generate 1s worth of samples
            freqs = np.fft.rfftfreq(sample_rate, 1.0/sample_rate)
            # initialize array for complex frequncies
            spectrum = np.zeros_like(freqs, dtype='complex')
            # apply power-law attenuation
            # (don't quite understand why we need a square root)
            spectrum[1:] = freqs[1:] ** (-0.5 * self.beta)
            # random phases for all frequencies except f=0
            phases = np.random.uniform(0, 2*np.pi, len(freqs)-1)
            spectrum[1:] *= np.exp(1j*phases)  # apply random phases
            noise = np.fft.irfft(spectrum)  # return the reverse fourier transform
            # rescale to desired amplitude range
            noise = minmax_scale(noise, (-self.amplitude, self.amplitude))

            self.__sample_buffer = deque(noise)

        # Pop from the buffer
        # Refill buffer if empty
        def generator_function(x):
            try:
                return self.__sample_buffer.popleft()
            except IndexError:
                pre_generate_samples()
                return self.__sample_buffer.popleft()
        super().__init__(sample_rate, generator_function=generator_function)
