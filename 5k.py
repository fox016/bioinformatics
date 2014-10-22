#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2

INDEL_COST = -5

PROTEIN_INDEX_MAP = {'A': 0, 'C': 1, 'E': 3, 'D': 2, 'G': 5, 'F': 4, 'I': 7, 'H': 6, 'K': 8, 'M': 10, 'L': 9, 'N': 11, 'Q': 13, 'P': 12, 'S': 15, 'R': 14, 'T': 16, 'W': 18, 'V': 17, 'Y': 19}

def max_alignment(v, w, matrix):
	op = -1
	row = [INDEL_COST * i for i in xrange(len(v)+1)]
	for j in xrange(1, len(w)+1):
		new_row = [(INDEL_COST * j)] + ([0] * len(v))
		for i in xrange(1, len(row)):
			new_row[i], op = max_index([new_row[i-1] + INDEL_COST, row[i] + INDEL_COST, row[i-1] + match_cost(v[i-1], w[j-1], matrix)])
		row = new_row
	return row[len(v)], op

def match_cost(p1, p2, matrix):
	return matrix[PROTEIN_INDEX_MAP[p1]][PROTEIN_INDEX_MAP[p2]]

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(1, len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

def linear_middle_edge(v, w, matrix):
	middle = len(w) / 2
	best = (0, float("-inf"), 0)
	for i in xrange(len(v)+1):
		source_dist = from_source(i, middle, v, w, matrix)[0]
		sink_dist, op = to_sink(i, middle, v, w, matrix)
		length = source_dist + sink_dist
		if length > best[1]:
			best = (i, length, op)
	op = best[2]
	if op == DELETE:
		return (best[0], middle), (best[0]+1, middle)
	elif op == INSERT:
		return (best[0], middle), (best[0], middle+1)
	return (best[0], middle), (best[0]+1, middle+1)

def from_source(row, col, v, w, matrix):
	return max_alignment(v[0:row], w[0:col], matrix)

def to_sink(row, col, v, w, matrix):
	return max_alignment(v[row-1:][::-1], w[col-1:][::-1], matrix)

matrix = [map(int, line.split()) for line in open("blosum62.txt", "r")]
v, w = [line[:-1] for line in open("input.txt", "r")]
print linear_middle_edge(w, v, matrix)
