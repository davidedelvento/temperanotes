from __future__ import division
from math import log, sqrt
import argparse, sys

def qfrequencies_raw(temperament, octaves_low, octaves_high, base_freq):
    freq = []
    for octave in range(1, octaves_low + 1):
        freq =  [(base_freq / 2 ** octave) * note for note in temperament] + freq
    for octave in range(octaves_high):
        freq += [(base_freq * 2 ** octave) * note for note in temperament]
    return freq

def qextra_notes(octaves):
    extra_notes = int( .01 + (octaves - int(octaves))  * 12)
    new_octaves = int(octaves)
    if extra_notes > 0:
        new_octaves += 1
    if extra_notes == 0:
        extra_notes = 12
    return extra_notes, new_octaves

def qfrequencies(temperament, octaves_low, octaves_high, base_freq = 440.0, key_freq = '7'):
    extra_notes_lo, o_l = extra_notes(octaves_low)
    extra_notes_hi, o_h = extra_notes(octaves_high)

    freq = frequencies_raw(temperament, o_l, o_h, base_freq)
    return freq[12 - extra_notes_lo:len(freq) + extra_notes_hi - 12]

#def frequencies(temperament, notes_low, notes_high, key = 'C', base_freq = 440.0, key_freq = 'A'):
def frequencies(temperament, notes_low, notes_high, base_freq = 440.0):
    freq = []
    for fullnote in range(notes_high):
        octave, note = divmod(fullnote, 12)
        freq.append((base_freq * 2 ** octave) * temperament[note])

    for fullnote in range(notes_low):
        octave, note = divmod(fullnote, 12)
        freq.append((base_freq / 2 ** octave) * temperament[note])

    return freq

def equal_temperament():
    return [ 2. ** (i/12)  for i in range(12)]

def to_cents(temperament):
    a = temperament[0]
    return [int(1200 * log(t / a, 2) + .5) for t in temperament]

def myeval(x, integer=False):
    e = None
    r = None
    try:
        if integer:
            r = int(eval(x) + .5)
        else:
            r = eval(x)
    except Exception as ex:
        e = ex
    return r, e

def verify(temp, cents):
    computed_cents = to_cents(temp)
    for i, c in enumerate(computed_cents):
        if c != cents[i]:
            print "Warning: cent different for", str(i) + "th element", c, "vs", cents[i]

def read_temperament(t):
    temp = []
    cents = []
    exceptions = []
    must_exit = False
    for line in t.splitlines(True):
        useful = line.split("#")[0].strip()
        if useful:
            stuff = useful.split(",")
            result, excp = myeval(stuff[0])
            temp.append(result)
            exceptions.append(excp)
            if len(stuff) == 2:
                result, excp = myeval(stuff[1], integer=True)
                cents.append(result)
                exceptions.append(excp)
            elif len(stuff) > 2:
                print >> sys.stderr, "Temperament file can not have more than 2 entries per line"
                print >> sys.stderr, "     instead it has in line:"
                print >> sys.stderr, line
                must_exit = True

    if len(temp) != 12:
        print >> sys.stderr, "Temperament file must have 12 entries for the chromatic scale"
        print >> sys.stderr, "     instead it has", len(temp)
        must_exit = True

    if len(cents) != 12 and len(cents) != 0:
        print >> sys.stderr, "Temperament file must have 0 or 12 entries for the chromatic scale"
        print >> sys.stderr, "     for the cents field. Instead it has", len(cents)
        must_exit = True

    real_exceptions = [value for value in exceptions if value is not None]
    if len(real_exceptions) > 0:
        print >> sys.stderr, "Problems reading temperament file"
        print >> sys.stderr, real_exceptions
        must_exit = True
    if must_exit:
        sys.exit(1)
    return temp, cents

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("temperament", type=argparse.FileType('r'),
                                       help="Temperament file, see README.md for details")
    args = parser.parse_args()
    temp, cents = read_temperament(args.temperament.read())
    verify(temp, cents)

    print "------------- trying to build a piano ---------------"
    piano = frequencies(temp, octaves_low = 4, octaves_high = 3 + 4./12)  # starts from A-440
    print "Number of key:", len(piano), "(should be 88)"
    print piano
    print "Index of the A-440", piano.index(440.), "(should be the 49th key or index 48)"

    print "------- trying to build a full MIDI keyboard --------"
    midi = frequencies(temp, octaves_low = 5 + 9./12, octaves_high = 4 + 10./12)
    print len(midi), "should be 128"
    print midi
    print "Index of the A-440", midi.index(440.), "(should be 69)"
