#!/usr/bin/python

def bw_matching(first_occurrence, bottom, pattern, count):
	top = 0
	while top <= bottom:
		if pattern:
			symbol = pattern[-1]
			pattern = pattern[:-1]
			top = first_occurrence[symbol] + count[symbol][top]
			bottom = first_occurrence[symbol] + count[symbol][bottom+1] - 1
		else:
			return bottom - top + 1
	return 0

def calc_last_to_first(first_col, index_map):
	last_to_first = [0] * len(last_col)
	for first_index in xrange(len(first_col)):
		char = first_col[first_index]
		last_index = index_map[char]
		last_to_first[last_index] = first_index
	return last_to_first

def calc_count(alpha, last_col):
	count = {}
	for char in alpha:
		current_count = 0
		count[char] = [0]
		for i in xrange(len(last_col)):
			if last_col[i][0] == char:
				current_count+=1
			count[char].append(current_count)
	return count

def calc_first_occurrence(first_col):
	first_occurrence = {}
	for i in xrange(len(first_col)):
		if first_col[i][0] not in first_occurrence:
			first_occurrence[first_col[i][0]] = i
	return first_occurrence

#read = [line[:-1] for line in open("/Users/Admin/Downloads/rosalind_7l.txt", "r")]
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

last_to_first = calc_last_to_first(first_col, index_map)
count = calc_count(set(bwt), last_col)
first_occurrence = calc_first_occurrence(first_col)

print ' '.join(map(lambda pattern: str(bw_matching(first_occurrence, len(last_col)-1, pattern, count)), patterns))
