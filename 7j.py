#!/usr/bin/python

bwt = [line[:-1] for line in open("input.txt", "r")][0]
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

solution = []
char = ('$', 1)
while len(solution) < len(bwt):
	solution.append(char[0])
	char = first_col[index_map[char]]
print ''.join(solution[1:])+"$"
