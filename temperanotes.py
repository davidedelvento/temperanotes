from __future__ import division
from math import log, sqrt
import argparse, sys

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
                                       help="Temperament file, see README.md for details"
    args = parser.parse_args()
    temp, cents = read_temperament(args.temperament.read())
    verify(temp, cents)
