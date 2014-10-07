#!/usr/bin/python

CONTINUE = 0
GO_UP = 1
GO_DOWN = 2

LOWER = 0
MIDDLE = 1
UPPER = 2

OPEN_COST = -11
EXT_COST = -1

PROTEIN_INDEX_MAP = {'A': 0, 'C': 1, 'E': 3, 'D': 2, 'G': 5, 'F': 4, 'I': 7, 'H': 6, 'K': 8, 'M': 10, 'L': 9, 'N': 11, 'Q': 13, 'P': 12, 'S': 15, 'R': 14, 'T': 16, 'W': 18, 'V': 17, 'Y': 19}

def max_alignment(v, w, matrix):
	lower_vals = []
	middle_vals = []
	upper_vals = []
	lower_ops = []
	middle_ops = []
	upper_ops = []
	for i in xrange(len(v)+1):
		lower_vals.append([0] * (len(w)+1))
		middle_vals.append([0] * (len(w)+1))
		upper_vals.append([0] * (len(w)+1))
		lower_ops.append([0] * (len(w)+1))
		middle_ops.append([0] * (len(w)+1))
		upper_ops.append([0] * (len(w)+1))
	for i in xrange(len(v)+1):
		lower_ops[i][0] = CONTINUE
		middle_ops[i][0] = GO_DOWN
		upper_ops[i][0] = GO_DOWN
		upper_vals[i][0] = float("-inf")
	for j in xrange(len(w)+1):
		lower_ops[0][j] = GO_UP
		middle_ops[0][j] = GO_UP
		upper_ops[0][j] = CONTINUE
		lower_vals[0][j] = float("-inf")
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			lower_vals[i][j], lower_ops[i][j] = max_index([lower_vals[i-1][j] + EXT_COST, \
									middle_vals[i-1][j] + OPEN_COST, \
									float("-inf")])
			upper_vals[i][j], upper_ops[i][j] = max_index([upper_vals[i][j-1] + EXT_COST, \
									float("-inf"),
									middle_vals[i][j-1] + OPEN_COST])
			middle_vals[i][j], middle_ops[i][j] = max_index([middle_vals[i-1][j-1] + match_cost(v[i-1], w[j-1], matrix), \
									upper_vals[i][j], \
									lower_vals[i][j]])
	print middle_vals[len(v)][len(w)]
	unwind_ops([lower_ops, middle_ops, upper_ops], v, w, len(v), len(w))

def unwind_ops(ops_list, v, w, i, j):
	new_v = []
	new_w = []
	layer = MIDDLE
	while i != 0 or j != 0:
		print i, j
		if ops_list[layer][i][j] == CONTINUE:
			if layer == LOWER:
				new_v.append(v[i-1])
				new_w.append("-")
				i-=1
			elif layer == MIDDLE:
				new_v.append(v[i-1])
				new_w.append(w[j-1])
				i-=1
				j-=1
			elif layer == UPPER:
				new_w.append(w[j-1])
				new_v.append("-")
				j-=1
		elif ops_list[layer][i][j] == GO_UP:
			if layer == LOWER:
				new_v.append(v[i-1])
				new_w.append("-")
				i-=1
			layer+=1
		elif ops_list[layer][i][j] == GO_DOWN:
			if layer == UPPER:
				new_w.append(w[j-1])
				new_v.append("-")
				j-=1
			layer-=1
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

matrix = [map(int, line.split()) for line in open("blosum62.txt", "r")]
v, w = [line[:-1] for line in open("input.txt", "r")][0:2]
max_alignment(v, w, matrix)
