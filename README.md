[![Build Status](https://travis-ci.org/davidedelvento/temperanotes.svg?branch=master)](https://travis-ci.org/davidedelvento/temperanotes)

# Temperanotes - Musical Temperament Editor
![Logo](https://github.com/davidedelvento/temperanotes/blob/master/logo.png)

Temperanotes is command line Musical Temperament Editor useful to transform temperament descriptions such as the ones found on wikipedia
(e.g. [Werckmeister temperament II](https://en.wikipedia.org/wiki/Werckmeister_temperament#Werckmeister_II_.28IV.29:_another_temperament_included_in_the_Orgelprobe.2C_divided_up_through_1.2F3_comma))
into practically usable formats, such as the input format for [timidity](http://timidity.sourceforge.net/) described 
[here](http://music.stackexchange.com/questions/12566/what-file-format-does-timiditys-z-or-freq-table-option-require), or a midi
[MTS](https://en.wikipedia.org/wiki/MIDI_Tuning_Standard) bulk tuning file, and likely even something like Pianoteq format (if the
specs can be found)

# Input files
The input temperament needs exactly 12 entries (lines). Comments are allowed on any line (entry or non-entry line) and must start with `#`.
Each entry line must be of the form:

```
frequency_ratio [, cent]
```

where both `frequency_ratio` and `cent` can be a python expression such as `sqrt(2)` or `103` or `2 ** (1/32)`. Note that `sqrt` and
`log` are automatically imported from `math`, and that floating point division is automatically performed even from integer input.
The cent value is optional and will be rounded to the closest integer.

If present on one entry, the cent value must be present for all 12 entries. The cent values are used only for validation, in that
if `frequency_ratio` and `cent` do not agree, a warning is printed.

# Usage
Simply run something like

```
python temperanotes.py input/Werckmeister_I_III.txt -t > Werckmeister_I_III.timidity
```

to generate the timidity frequency file, which can be then used as argument file for the `--freq-table` option when invoking `timidity`.

# Details
At the moment I'm focusing on Meantone and Well Temperaments from the late 1600s to the early 1700s and on timidity only, but I may expand to other eras and software later (and pull request will always be welcome)

# Name and Logo
Temperanotes name is a [portmanteau](https://en.wikipedia.org/wiki/Portmanteau) of [temperament](https://en.wikipedia.org/wiki/Musical_temperament) and [note](https://en.wikipedia.org/wiki/Musical_note).

The logo is an Italian [tongue in cheek](https://en.wikipedia.org/wiki/Tongue-in-cheek) since in Italian *temperare* (the act of creating a temperament) means more commonly sharpening a pencil.
