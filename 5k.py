#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2

INDEL_COST = -5

PROTEIN_INDEX_MAP = {'A': 0, 'C': 1, 'E': 3, 'D': 2, 'G': 5, 'F': 4, 'I': 7, 'H': 6, 'K': 8, 'M': 10, 'L': 9, 'N': 11, 'Q': 13, 'P': 12, 'S': 15, 'R': 14, 'T': 16, 'W': 18, 'V': 17, 'Y': 19}

def max_alignment(v, w, matrix):
	row = [INDEL_COST * i for i in xrange(len(v)+1)]
	col = [INDEL_COST * j for j in xrange(len(w)+1)]
	for i in xrange(len(row)):
		for j in xrange(len(col)):

	"""
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			table[i][j] = max_index([table[i-1][j] + INDEL_COST, \
					table[i][j-1] + INDEL_COST, \
					table[i-1][j-1] + match_cost(v[i-1], w[j-1], matrix)])
	return table[len(v)][len(w)]
	"""

def match_cost(p1, p2, matrix):
	return matrix[PROTEIN_INDEX_MAP[p1]][PROTEIN_INDEX_MAP[p2]]

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(1, len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best[0]

def get_middle_node(v, w, matrix):
	n = len(v)
	m = len(w)
	middle = m / 2
	best = (0, float("-inf"))
	for i in xrange(n+1):
		length = from_source(i, middle, v, w, matrix) + to_sink(i, middle, v, w, matrix)
		if length > best[1]:
			best = (i, length)
	return (best[0], middle)

def from_source(row, col, v, w, matrix):
	pass # TODO

def to_sink(row, col, v, w, matrix):
	pass # TODO

def linear_middle_edge(v, w, matrix):
	middle_node = get_middle_node(v, w, matrix)

matrix = [map(int, line.split()) for line in open("blosum62.txt", "r")]
v, w = [line[:-1] for line in open("input.txt", "r")]
print linear_middle_edge(v, w, matrix)
