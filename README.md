# Tab-maker

This program is intended to produce guitar tabs from midi files such that the total number of horizontal moves of the fretting hand is kept minimal.

# Background

We enumerate hand positions from neck to body starting from 1 to 12. By hand position we mean the position of the index finger. 

1. We assume that there is a fixed number of frets the hand can reach horizontally at any horizontal position, the default value is 4.
2. We assume that the exact same note (the unison) is never played on different strings.
3. We assume that the hand position cannot be changed during the playing of a fretted note (not an open string).
4. We assume that the midi file consists of a single track.

Under these assumptions our code outputs a tablature which shows when to change the hand position to where. The solution is optimum in the sense that it minimizes the number of hand position changes.

# Algorithm
In the following, midi events refer to 'note_on' or 'note_off' events. Let e_i be the i^{th} midi event in the input. Let S_i be the notes that are playing at the after the i^{th} event. We define a bag to be the union S_i + S_{i+1} + ... + S_j such that S_i and S_j are both playable with open strings only (or possibly empty).