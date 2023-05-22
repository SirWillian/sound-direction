import csv
import sys
from functools import reduce
from os import makedirs
from os.path import abspath, basename, dirname, join, realpath, splitext

import numpy as np
from scipy.io import wavfile

project_root_path = realpath(join(abspath(dirname(__file__)), '..'))
out_path = join(project_root_path, "tests", "output")
sys.path.insert(0, project_root_path)

from PowerLawNoiseSoundSource import PowerLawNoiseSoundSource
from WavFileSoundSource import WavFileSoundSource
from WhiteNoiseSoundSource import WhiteNoiseSoundSource


def load_sample(name: str, volume_factor: int = 1) -> WavFileSoundSource:
    return WavFileSoundSource(join(project_root_path, "samples", name + ".wav"), volume_factor)

def get_test_name(filename: str) -> str:
    return splitext(basename(filename))[0]

def get_output_path() -> str:
    return out_path

def create_test_writer(test_name: str):
    makedirs(join(out_path, test_name), exist_ok=True)
    outfile = open(join(out_path, test_name, test_name+'.csv'), 'w', newline='')
    csvwriter = csv.writer(outfile)
    return (outfile, csvwriter)

def save_wav_samples(samples, sample_rate, sample_name, test_name, *test_vars):
    makedirs(join(out_path, test_name), exist_ok=True)
    x = np.int16(np.array(samples) * (2**15 - 1))
    out_prefix = ""
    if (len(test_vars)):
        out_prefix = reduce(lambda x,y: x+"-"+y, test_vars)+"-"
    wavfile.write(f'{join(out_path, test_name, out_prefix+sample_name)}.wav', sample_rate, x)

def calc_angle_error(ang1, ang2) -> float:
    return abs(((ang1 - ang2) + 180) % 360 - 180)

def create_noise_source(noise_type: str, sample_rate: int, amplitude=1.0, beta=1):
    if noise_type == "white":
        return WhiteNoiseSoundSource(sample_rate, amplitude)
    elif noise_type == "pink":
        return PowerLawNoiseSoundSource(sample_rate, beta, amplitude)
    else:
        return None