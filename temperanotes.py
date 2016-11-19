def frequencies(temperament, low, high, base_freq = 440.0):
    freq = []
    for octave in range(2, low + 2):
        freq =  [(base_freq / octave) * note for note in temperament] + freq
    for octave in range(1, high + 1):
        freq += [(base_freq * octave) * note for note in temperament]
    return freq
