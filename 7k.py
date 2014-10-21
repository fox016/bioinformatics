#!/usr/bin/python

def bw_matching(last_col, pattern, last_to_first):
	top = 0
	bottom = len(last_col)-1
	while top <= bottom:
		if pattern:
			symbol = pattern[-1]
			pattern = pattern[:-1]
			if symbol in last_col[top:bottom+1]:
				top, bottom = last_to_first[top+last_col[top:bottom+1].index(symbol)], last_to_first[bottom - last_col[top:bottom+1][::-1].index(symbol)]
			else:
				return 0
		else:
			return bottom - top + 1

read = [line[:-1] for line in open("input.txt", "r")]
bwt = read[0]
patterns = read[1].split()

char_count_map = {}
last_col = []
index_map = {}
for char in bwt:
	if char not in char_count_map:
		char_count_map[char] = 1
	else:
		char_count_map[char] += 1
	index_map[(char, char_count_map[char])] = len(last_col)
	last_col.append((char, char_count_map[char]))
first_col = sorted(last_col)

last_to_first = [0] * len(last_col)
for first_index in xrange(len(first_col)):
	char = first_col[first_index]
	last_index = index_map[char]
	last_to_first[last_index] = first_index

print ' '.join(map(lambda pattern: str(bw_matching(map(lambda c: c[0], last_col), pattern, last_to_first)), patterns))
