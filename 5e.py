#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2

INDEL_COST = -5

PROTEINS = "ACDEFGHIKLMNPQRSTVWY"

def max_alignment(v, w, matrix):
	table = []
	ops = []
	for i in xrange(len(v)+1):
		table.append([0] * (len(w)+1))
		ops.append([0] * (len(w)+1))
	for i in xrange(len(v)+1):
		table[i][0] = INDEL_COST * i
		ops[i][0] = DELETE
	for j in xrange(len(w)+1):
		table[0][j] = INDEL_COST * j
		ops[0][j] = INSERT
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			table[i][j], ops[i][j] = max_index([table[i-1][j] + INDEL_COST, \
					table[i][j-1] + INDEL_COST, \
					table[i-1][j-1] + match_cost(v[i-1], w[j-1], matrix)])
	return table[len(v)][len(w)], w, unwind_ops(ops, v, len(v), len(w))

def unwind_ops(ops, v, i, j):
	chars = []
	while i != 0 or j != 0:
		if ops[i][j] == DELETE:
			i-=1
		elif ops[i][j] == INSERT:
			j-=1
			chars.append("-")
		else:
			chars.append(v[i-1])
			i-=1
			j-=1
	return ''.join(chars[::-1])

def match_cost(p1, p2, matrix):
	return matrix[PROTEINS.index(p1)][PROTEINS.index(p2)]

def max_index(nums):
	best = (float("-inf"), float("-inf"))
	for index in xrange(len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

matrix = [map(int, line.split()) for line in open("blosum62.txt", "r")]
w, v = [line[:-1] for line in open("input.txt", "r")]
print '\n'.join(map(str, max_alignment(v, w, matrix)))
