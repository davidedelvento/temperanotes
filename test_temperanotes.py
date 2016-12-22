import temperanotes
import pytest

@pytest.fixture
def idiot_temp():
    temp = [1, 1.05, 1.1, 1.15, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]            # not a temperament, just a set of numbers for testing
    assert len(temp) == 12                                                         # need 12 notes for the chromatic scale
    return temp

def test_note_names():
    exclude = ['B#', 'Cb', 'E#', 'Fb']
    assert len(temperanotes.note_names_sharp) == 12
    assert len(temperanotes.note_names_flat) == 12
    for note in "ABCDEFG":
        assert note in temperanotes.note_names_sharp
        assert note in temperanotes.note_names_flat
        note_accidental = note + "#"
        if not note_accidental in exclude:
            assert note_accidental in temperanotes.note_names_sharp
        note_accidental = note + "b"
        if not note_accidental in exclude:
            assert note_accidental in temperanotes.note_names_flat

def test_get_key_index():
    assert temperanotes.get_key_index('A') == 0
    assert temperanotes.get_key_index('C') == 3
    assert temperanotes.get_key_index('F') == 8
    assert temperanotes.get_key_index('F#') == 9
    assert temperanotes.get_key_index('G#') == 11
    assert temperanotes.get_key_index('Ab') == 11

def test_normal_octave_in_C(idiot_temp):
    # when starting from C,
    # A is the 10th semitone of the chromatic scale, i.e. idiot_temp[9]
    expected_freq = [440.0 / idiot_temp[9] * i for i in idiot_temp]
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 0, notes_high = 12, key = 'C', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_normal_octave(idiot_temp):
    expected_freq = [440.0 * i for i in idiot_temp]
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 0, notes_high = 12, key = 'A', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_lower_octave(idiot_temp):
    expected_freq = [440.0 / 2 * i for i in idiot_temp]
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 12, notes_high = 0, key = 'A', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_one_octave_and_one_note(idiot_temp):
    expected_freq = [440.0     * i for i in idiot_temp] + [440.0 * 2]
    assert len(expected_freq) == 13                                                    # obvious, but making sure no simply bugs in test itself
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 0, notes_high = 13, key = 'A', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_one_octave_and_one_note_per_direction(idiot_temp):
    expected_freq_lo   = [440.0 / 2 * i for i in idiot_temp]
    expected_freq_hi   = [440.0     * i for i in idiot_temp]
    expected_freq = [440.0 / 4 * idiot_temp[-1]] + expected_freq_lo + expected_freq_hi + [440.0 * 2]
    assert len(expected_freq) == 24 + 2                                                 # obvious, but making sure no simply bugs in test itself
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 13, notes_high = 13, key = 'A', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_one_octave_and_half_per_direction(idiot_temp):
    expected_freq_lolo = [440.0 / 4 * i for i in idiot_temp]
    expected_freq_lo   = [440.0 / 2 * i for i in idiot_temp]
    expected_freq_hi   = [440.0     * i for i in idiot_temp]
    expected_freq_hihi = [440.0 * 2 * i for i in idiot_temp]
    expected_freq = expected_freq_lolo[6:] + expected_freq_lo + expected_freq_hi + expected_freq_hihi[:6]
    assert len(expected_freq) == 48 - 12                                                 # obvious, but making sure no simply bugs in test itself
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 18, notes_high = 18, key = 'A', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_two_octaves(idiot_temp):
    expected_freq_lo = [440.0 / 2 * i for i in idiot_temp]
    expected_freq_hi = [440.0     * i for i in idiot_temp]
    expected_freq = expected_freq_lo + expected_freq_hi
    assert len(expected_freq) == 24                                                      # obvious, but making sure no simply bugs in test itself
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 12, notes_high = 12, key = 'A', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_four_octaves(idiot_temp):
    expected_freq_lolo = [440.0 / 4 * i for i in idiot_temp]
    expected_freq_lo   = [440.0 / 2 * i for i in idiot_temp]
    expected_freq_hi   = [440.0     * i for i in idiot_temp]
    expected_freq_hihi = [440.0 * 2 * i for i in idiot_temp]
    expected_freq = expected_freq_lolo + expected_freq_lo + expected_freq_hi + expected_freq_hihi
    assert len(expected_freq) == 48                                                      # obvious, but making sure no simply bugs in test itself
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, notes_low = 24, notes_high = 24, key = 'A', base_freq = 440.0, key_freq = 'A')
    assert actual_freq == expected_freq

def test_equal_temp():
    expected = [1., 2. ** (1./12), 2. ** (1./6), 2. ** (1./4), 2. ** (1./3), 2. ** (5./12), 2. ** (1./2), 2. ** (7./12), 2. ** (2./3), 2. ** (3./4), 2. ** (5./6), 2. ** (11./12)]
    actual = temperanotes.equal_temperament()
    assert actual == expected

def test_cents():
    expected = [100 * i for i in range(12)]
    actual = temperanotes.to_cents(temperanotes.equal_temperament())
    assert actual == expected

def test_read_temperament_nocents():
    data = """#This is a comment
              1
              1.01 # this is another comment
              1.3
              1.4
              # more comments
              1.5
              1.6
              1.7
              1.8
              1.9
              1.10
              1.11
              1.12"""
    expected = [1, 1.01, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11, 1.12]
    actual, cents = temperanotes.read_temperament(data)
    assert actual == expected
    assert len(cents) == 0

def test_read_temperament_withcents_and_math():
    data = """#This is a comment
              1, 100
              sqrt(2), 200 # this is another comment
              1.3, 4 ** (1/3)   # 1.58 must round to 2
              2 ** 1/12, 500
              # more comments
              1.5, 600
              1.6, 700
              1.7, 900
              1.8, 1000
              1.9, 2000  # comments can appear anywhere
              1.10, 3000
              1.11, 1
              1.12, 7
              # comments at the end"""
    expected = [1, 1.4142135623730951, 1.3, 0.1666666666666666666666666, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11, 1.12]
    actual, cents = temperanotes.read_temperament(data)
    assert actual == expected
    assert cents == [100, 200, 2, 500, 600, 700, 900, 1000, 2000, 3000, 1, 7]

def test_read_incorrect_temperaments():
    data = 11 * "1, 100\n"
    with pytest.raises(SystemExit):
        temperanotes.read_temperament(data)
    data = 13 * "1, 100\n"
    with pytest.raises(SystemExit):
        temperanotes.read_temperament(data)

def test_read_more_entries_cents():
    data = (5 * "1, 100\n" +
            2 * "2, 150, 200\n" +   # additional data
            5 * "7, 200\n")
    with pytest.raises(SystemExit):
        temperanotes.read_temperament(data)

def test_read_incorrect_cents():
    data = (5 * "1, 100\n" +
            2 * "2,\n" +            # missing some cents (with comma)
            5 * "7, 200\n")
    with pytest.raises(SystemExit):
        temperanotes.read_temperament(data)

def test_read_missing_cents():
    data = (5 * "1, 100\n" +
            2 * "2\n" +             # missing some cents (without comma)
            5 * "7, 200\n")
    with pytest.raises(SystemExit):
        temperanotes.read_temperament(data)

def test_read_file_with_errors():
    data = (5 * "1, 100\n" +
            2 * "foo_bar, 200\n" +  # syntax error in frequencies
            5 * "7, 700\n")
    with pytest.raises(SystemExit):
        temperanotes.read_temperament(data)
    data = (5 * "1, 100\n" +
            2 * "2, foo_bar\n" +    # syntax error in cents
            5 * "7, 700\n")
    with pytest.raises(SystemExit):
        temperanotes.read_temperament(data)

# not testing verify() since it's very simple
# not explicitly testing myeval() since it's implicitly tested in each read_temperament() invocation
