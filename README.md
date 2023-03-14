# Tab-maker

This program is intended to produce guitar tabs from midi files such that the total number of horizontal moves of the fretting hand is kept minimal.

# Background

We enumerate hand positions from neck to body starting from 1 to 12. By hand position we mean the position of the index finger. 

1. We assume that there is a fixed number of frets the hand can reach horizontally at any horizontal position, the default value is 4.
2. We assume that the exact same note (the unison) is never played on different strings at the same time.
3. We assume that the hand position cannot be changed during the playing of a fretted note (not an open string).
4. We assume that the midi file consists of a single track.

Under these assumptions our code outputs a tablature which shows when to change the hand position to where. The solution is optimum in the sense that it minimizes the number of horizontal hand position changes.

# Algorithm
In the following, we concern only 'note_on' and 'note_off' events in the input. Let $l$ denote the number of events in the loop. We say that $i$ is an eligible position if the set of all notes that are still playing after the $i^{th}$ midi event is a subset of open strings. Note that 0 and $l$ are always eligible positions.


On the $i^{th}$ iteration of the loop:
1. Check if it is an eligible position. If not, move on to the next iteration.
2. Compute the set of all hand positions $H_i$ that can play the part of the tune since the last eligible position, starting with the set of notes still playing at the last eligible position.
3. Let $i'$ be the previous eligible position. If $H_i \cap H_{i'}$ is not empty, assign the intersection set to $H_i$. Else, mark $i$ to be a hand move position, and pick $h \in H_i$ and $h' \in H_{i'}$ such that $|h-h'|$ is minimized.
