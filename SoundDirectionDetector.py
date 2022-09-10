import logging
import math
from typing import List

import numpy as np
from numpy.typing import NDArray
from scipy import signal

from Microphone import Microphone


class SoundDirectionDetector:
    microphones: List[Microphone]

    def __init__(self, sample_rate=44100, speed_of_sound=343, sample_count=44100, sample_time_window=0) -> None:
        self.logger = logging.getLogger('direction-detector')
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())
        self.microphones = []
        self.sample_rate = sample_rate
        self.speed_of_sound = speed_of_sound
        if (sample_time_window == 0):
            self.sample_count = sample_count
        else:
            self.sample_count = int(sample_time_window * sample_rate)

    def add_microphone(self, microphone: Microphone) -> None:
        self.microphones.append(microphone)

    def detect_sound_direction(self, method='tdoa') -> float:
        if (method == 'tdoa'):
            #tdoa_0i = np.empty(len(self.microphones)-1, dtype=[('direction', 'f4'), ('lag', 'i4')])
            # Calculate the TDOA between each mic. There are only N-1 independent cross-correlations between mics
            # Use these cross-correlations to find TDOAs in relation to the first mic
            tdoa_0i = np.empty(len(self.microphones)-1)
            for i in range(1, len(self.microphones)):
                m0_samples: NDArray[np.float32]
                mi_samples: NDArray[np.float32]
                m0_samples = np.array(self.microphones[0].samples)[-self.sample_count:]
                mi_samples = np.array(self.microphones[i].samples)[-self.sample_count:]
                self.logger.debug("m0 max %s m0 min %s mi max %s mi min %s", np.max(m0_samples), np.min(m0_samples), np.max(mi_samples), np.min(mi_samples))
                # Calculate the cross-correlation between samples and take the delay
                # on the correlation peak
                cross_correlation = signal.correlate(m0_samples, mi_samples, mode="full")
                lags = signal.correlation_lags(m0_samples.size, mi_samples.size, mode="full")
                # negative lag means that m0 received the sound earlier than mi
                #lag = lags[np.argmax(cross_correlation)]

                # Determine max possible lag based on distance between mics and check for correlation peaks within that range
                max_lag = math.ceil(((np.linalg.norm(self.microphones[0].position - self.microphones[i].position)) / self.speed_of_sound) * self.sample_rate)
                self.logger.debug("max lag %d", max_lag)
                possible_lags_mask = abs(lags) <= max_lag
                top_value_args = (-(cross_correlation[possible_lags_mask])).argsort()[:7]
                top_lags = lags[possible_lags_mask][top_value_args]
                lag = top_lags[0]
                self.logger.debug("top lags %s top values %s", top_lags, cross_correlation[possible_lags_mask][top_value_args])
                self.logger.debug("lag %d m0 %s mi %s dist %f", lag, self.microphones[0].position, self.microphones[i].position, np.linalg.norm(self.microphones[0].position - self.microphones[i].position))
                #self.logger.debug(math.acos((self.speed_of_sound * (lag / self.sample_rate))))
                #direction = np.rad2deg(math.acos((self.speed_of_sound * (lag / self.sample_rate)) /
                #                       np.linalg.norm(self.microphones[0].position - self.microphones[i].position)))
                #tdoa_0i[i-1] = (direction, lag)
                tdoa_0i[i-1] = lag
            
            if (len(self.microphones) > 2):
                # dot(vec(u), vec(x_ij)) = speed_of_sound * tdoa_ij
                # vec(u) is the sound direction
                # vec(x_ij) is the vector from j to i (x_j - x_i, y_j - y_i, z_j - z_i)
                # tdoa_ij is the lag between mics i and j
                # apply the equation on each independent mic pair and solve the linear system of all of them combined
                A = np.array([mic.position - self.microphones[0].position for mic in self.microphones[1:]])
                B = self.speed_of_sound*np.array(tdoa_0i)/self.sample_rate
                #self.logger.debug("tdoa", tdoa_0i)
                #self.logger.debug("A", A)
                #self.logger.debug("B", B)
                sound_pos = np.linalg.lstsq(A,B,rcond=None)[0]
                self.logger.debug("sound_pos %s", sound_pos)
                return math.degrees(math.atan2(sound_pos[1], sound_pos[0]))
            return tdoa_0i
        return 0.0
