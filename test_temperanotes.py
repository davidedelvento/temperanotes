import temperanotes
import pytest

@pytest.fixture
def idiot_temp():
    temp = [1, 1.05, 1.1, 1.15, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]            # not a temperament, just a set of numbers for testing
    assert len(temp) == 12                                                         # need 12 notes for the chromatic scale
    return temp

def test_two_octaves(idiot_temp):
    expected_freq_lo = [440.0 / 2 * i for i in idiot_temp]
    expected_freq_hi = [440.0     * i for i in idiot_temp]
    expected_freq = expected_freq_lo + expected_freq_hi
    assert len(expected_freq) == 24                                                      # obvious, but making sure no simply bugs in test itself
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, low = 1, high = 1)
    assert actual_freq == expected_freq

def test_normal_octave(idiot_temp):
    expected_freq = [440.0 * i for i in idiot_temp]
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, low = 0, high = 1)
    assert actual_freq == expected_freq

def test_lower_octave(idiot_temp):
    expected_freq = [440.0 / 2 * i for i in idiot_temp]
    actual_freq = temperanotes.frequencies(temperament = idiot_temp, low = 1, high = 0)
    assert actual_freq == expected_freq
