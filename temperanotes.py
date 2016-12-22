from __future__ import division
from math import log, sqrt
import argparse, sys

note_names_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
note_names_flat  = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

def get_key_index(key):
    if len(key) == 1:
        key_index = note_names_sharp.index(key)
    else:
        if key in note_names_sharp:
            key_index = note_names_sharp.index(key)
        else:
            key_index = note_names_flat.index(key)      # let it fail here, if a wrong note name was specified
    return key_index


def frequencies(temperament, notes_low, notes_high, key = 'C', base_freq = 440.0, key_freq = 'A'):
    key_index     = get_key_index(key)
    keyfreq_index = get_key_index(key_freq)
    use_base_freq = base_freq / temperament[keyfreq_index - key_index]
    freq = []
    for fullnote in range(-notes_low, notes_high):
        octave, note = divmod(fullnote, 12)
        freq.append((use_base_freq * 2 ** octave) * temperament[note])
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
    piano = frequencies(temp, notes_low = 4*12, notes_high = 3*12 + 4)  # starts from A-440
    print "Number of key:", len(piano), "(should be 88)"
    print piano
    print "Index of the A-440", piano.index(440.), "(should be the 49th key or index 48)"

    print "------- trying to build a full MIDI keyboard --------"
    midi = frequencies(temp, notes_low = 5*12 + 9, notes_high = 4*12 + 11)
    print len(midi), "should be 128"
    print midi
    print "Index of the A-440", midi.index(440.), "(should be 69)"
