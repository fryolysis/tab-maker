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
2. Compute the set of all hand positions that can play the part of the tune since the last eligible position.
3. Construct a set $S_i$ of tuples $(h_{ij}, r_{ij}, p_i)$ where $h_{ij}$ are the hand positions computed in step 2, $p_i$ is a pointer to the tuple $t \in S_{i'}$ where $i'$ is the previous eligible position and $t = (h,r,p)$ is the tuple with the lowest rank $r$. Set $r_{ij} = r$ if $h_{ij} = h$ and $r_{ij} = r + 1$ else. Set $r_{ij} = 0$ and $p_i = null$ if the previous eligible position is 0.

At the end of the loop, backtrack using the pointers starting from the tuple with the lowest rank in $S_l$. Rank corresponds to the number of total horizontal hand shifts since the beginning, so during the backtracking one can determine at which instants of the tune hand positions are changed.

Note that $S_0$ does not contain any element, and if there is some empty set $S_k$ with $k>0$ it indicates the impossibility of playing the tune.
