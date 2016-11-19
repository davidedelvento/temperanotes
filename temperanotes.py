from __future__ import division
import math
import argparse

def frequencies(temperament, octaves_low, octaves_high, base_freq = 440.0):
    freq = []
    for octave in range(1, octaves_low + 1):
        freq =  [(base_freq / 2 ** octave) * note for note in temperament] + freq
    for octave in range(octaves_high):
        freq += [(base_freq * 2 ** octave) * note for note in temperament]
    return freq

def equal_temperament():
    return [ 2. ** (i/12)  for i in range(12)]

def to_cents(temperament):
    a = temperament[0]
    return [int(1200 * math.log(t / a, 2) + .5) for t in temperament]

def read_temperament(t):
    for line in t.splitlines(True):
        print line,

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("temperament", type=argparse.FileType('r'),
                                       help="""File with exactly 12 lines (not counting comment
                                               lines, starting with #) specifying on each line
                                               "frequency_ratio_[,_cent]" where both frequency
                                               ratio and cent can be a python expression such
                                               as math.sqrt(2) or 103. The cent value is optional
                                               and will be rounded to the closest integer""")
    args = parser.parse_args()
    temp = read_temperament(args.temperament.read())
