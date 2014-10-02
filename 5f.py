#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2
FREE = 3

INDEL_COST = -5

PROTEIN_INDEX_MAP = {'A': 0, 'C': 1, 'E': 3, 'D': 2, 'G': 5, 'F': 4, 'I': 7, 'H': 6, 'K': 8, 'M': 10, 'L': 9, 'N': 11, 'Q': 13, 'P': 12, 'S': 15, 'R': 14, 'T': 16, 'W': 18, 'V': 17, 'Y': 19}

def max_alignment(v, w, matrix):
	table = []
	ops = []
	for i in xrange(len(v)+1):
		table.append([0] * (len(w)+1))
		ops.append([0] * (len(w)+1))
	for i in xrange(len(v)+1):
		ops[i][0] = DELETE
	for j in xrange(len(w)+1):
		ops[0][j] = INSERT
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			table[i][j], ops[i][j] = max_index([table[i-1][j] + INDEL_COST, \
					table[i][j-1] + INDEL_COST, \
					table[i-1][j-1] + match_cost(v[i-1], w[j-1], matrix), \
					0])
	print table[len(v)][len(w)]
	unwind_ops(ops, v, w, len(v), len(w))

def unwind_ops(ops, v, w, i, j):
	new_v = []
	new_w = []
	while i != 0 or j != 0:
		if ops[i][j] == DELETE:
			new_v.append(v[i-1])
			i-=1
			new_w.append("-")
		elif ops[i][j] == INSERT:
			new_w.append(w[j-1])
			j-=1
			new_v.append("-")
		elif ops[i][j] == MATCH:
			new_v.append(v[i-1])
			new_w.append(w[j-1])
			i-=1
			j-=1
		else:
			i=0
			j=0
	print ''.join(new_v[::-1])
	print ''.join(new_w[::-1])

def match_cost(p1, p2, matrix):
	return matrix[PROTEIN_INDEX_MAP[p1]][PROTEIN_INDEX_MAP[p2]]

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(1, len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

matrix = [map(int, line.split()) for line in open("pam250.txt", "r")]
v, w = [line[:-1] for line in open("input.txt", "r")]
max_alignment(v, w, matrix)
