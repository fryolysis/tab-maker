import heapq
from dataclasses import dataclass
from mido import MidiFile

# Midi Note 40 corresponds to E2

HAND_COVERAGE = 4
FRETS_PER_STRING = 12
open_strings = [i+40 for i in [0,5,10,15,19,24]] # standard tuning

tune = []

@dataclass(order=True)
class BagItem:
    rank: int
    hand_pos: int
    tune_pos: int
    parent: None
    delete: bool

@dataclass()
class NoteEvent:
    note: int
    is_on: bool


# input from midi file
midi_file = MidiFile('test.mid')

assert len(midi_file.tracks) == 1
track = midi_file.tracks[0]

for msg in track:
    if msg.type == 'note_on' and msg.velocity == 0:
        tune.append(NoteEvent(msg.note, False))
    elif msg.type == 'note_on':
        tune.append(NoteEvent(msg.note, True))
    elif msg.type == 'note_off':
        tune.append(NoteEvent(msg.note, False))


''' returns the set of all hand positions that can play the given range of tune '''
def get_hand_pos(note):
    res = set()
    for h in range(1,FRETS_PER_STRING):
        for s in open_strings:
            if (s+h <= note and note <= s+h+HAND_COVERAGE-1) or note == s:
                res.add(h)
                break
    return res

# we make the assumption that hand positions can change only when all notes except open strings are off
# we further assume that the same note is never played simultaneously on different strings
cur_notes = set()
# TODO: don't forget that the initial position is always eligible for hand position change!
bag = [BagItem(0,h,None,False,0) for h in get_hand_pos(tune[0])]
heapq.heapify(bag)

for i in range(len(tune)):
    e = tune[i]
    if e.is_on:
        cur_notes.add(e.note)
    else:
        cur_notes.remove(e.note)
    if cur_notes.difference(open_strings):
        continue

    # remove marked items
    (bag.remove(i) for i in bag if i.delete)

    new_hand_pos = get_hand_pos(cur_notes)
    bag_positions = set([i.hand_pos for i in bag])
    # mark items for deletion
    for i in bag:
        if i.hand_pos not in new_hand_pos:
            i.delete = True
    # add new items
    for h in new_hand_pos - bag_positions:
        item = BagItem(bag[0].rank + 1, h, bag[0], False, mel_pos)
        heapq.heappush(bag, item)






bag = [BagItem(0,h,None,False,0) for h in get_hand_pos(melody[0])]
heapq.heapify(bag)

for mel_pos in range(1,len(melody)):
    # remove marked items
    for i in bag:
        if i.delete:
            bag.remove(i)

    new_hand_pos = get_hand_pos(melody[mel_pos])
    bag_positions = set([i.hand_pos for i in bag])
    # mark items for deletion
    for i in bag:
        if i.hand_pos not in new_hand_pos:
            i.delete = True
    # add new items
    for h in new_hand_pos - bag_positions:
        item = BagItem(bag[0].rank + 1, h, bag[0], False, mel_pos)
        heapq.heappush(bag, item)

# remove marked items if any left
for i in bag:
    if i.delete:
        bag.remove(i)

# backpropagation
res = []
cur = bag[0]
while cur is not None:
    res.append(cur)
    cur = cur.parent

# modify melody
for i in res:
    melody.insert(i.mel_pos, i)

# print
for i in melody:
    print(i)