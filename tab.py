import heapq
from dataclasses import dataclass

HAND_COVERAGE = 4
FRETS_PER_STRING = 12
open_strings = [0,5,10,15,19,24] # standard tuning

melody = [18,19,22,23,25,26,29,30]


@dataclass(order=True)
class BagItem:
    rank: int
    hand_pos: int
    parent: None
    delete: bool
    mel_pos: int

def get_hand_pos(note):
    res = set()
    for h in range(1,FRETS_PER_STRING):
        for s in open_strings:
            if (s+h <= note and note <= s+h+HAND_COVERAGE-1) or note == s:
                res.add(h)
                break
    return res


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