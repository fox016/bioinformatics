#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2

INDEL_COST = -5

PROTEIN_INDEX_MAP = {'A': 0, 'C': 1, 'E': 3, 'D': 2, 'G': 5, 'F': 4, 'I': 7, 'H': 6, 'K': 8, 'M': 10, 'L': 9, 'N': 11, 'Q': 13, 'P': 12, 'S': 15, 'R': 14, 'T': 16, 'W': 18, 'V': 17, 'Y': 19}

def max_alignment(v, w, matrix):
	row = [INDEL_COST * i for i in xrange(len(v)+1)]
	ops = [INSERT for i in xrange(len(v)+1)]
	for j in xrange(1, len(w)+1):
		new_row = [(INDEL_COST * j)] + ([0] * len(v))
		for i in xrange(1, len(row)):
			new_row[i], ops[i] = max_index([new_row[i-1] + INDEL_COST, row[i] + INDEL_COST, row[i-1] + match_cost(v[i-1], w[j-1], matrix)])
		row = new_row
	return row, ops

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
	source_distances, source_ops = max_alignment(v, w[0:middle], matrix)
	sink_distances, sink_ops = max_alignment(v[::-1], w[middle-1:][::-1], matrix)
	best = (0, float("-inf"), 0)
	for i in xrange(1, len(v)+1):
		length = source_distances[i] + sink_distances[len(v)+1-i]
		if length > best[1]:
			best = (i, length, sink_ops[len(v)+1-i])
	op = best[2]
	if op == DELETE:
		return (best[0], middle), (best[0]+1, middle)
	elif op == INSERT:
		return (best[0], middle), (best[0], middle+1)
	return (best[0], middle), (best[0]+1, middle+1)

matrix = [map(int, line.split()) for line in open("blosum62.txt", "r")]
v, w = [line[:-1] for line in open("input.txt", "r")]
edge = linear_middle_edge(v, w, matrix)
print str(edge[0]) + " " + str(edge[1])
