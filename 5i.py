#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2
FREE = 3

INDEL_COST = -2

def max_alignment(v, w):
	table = []
	ops = []
	for i in xrange(len(v)+1):
		table.append([0] * (len(w)+1))
		ops.append([0] * (len(w)+1))
	for i in xrange(len(v)+1):
		ops[i][0] = FREE
	for j in xrange(len(w)+1):
		table[0][j] = INDEL_COST * j
		ops[0][j] = INSERT
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			table[i][j], ops[i][j] = max_index([table[i-1][j] + INDEL_COST, \
					table[i][j-1] + INDEL_COST, \
					table[i-1][j-1] + match_cost(v[i-1], w[j-1]), \
					table[0][j]])
	max_w = 0
	for index in xrange(len(w)+1):
		if table[len(v)][index] > table[len(v)][max_w]:
			max_w = index
	print table[len(v)][max_w]
	unwind_ops(ops, v, w, len(v), max_w)

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
			i = 0
	print ''.join(new_v[::-1])
	print ''.join(new_w[::-1])

def match_cost(p1, p2):
	return 1 if p1 == p2 else INDEL_COST

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(1, len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

v, w = [line[:-1] for line in open("input.txt", "r")]
max_alignment(v, w)
