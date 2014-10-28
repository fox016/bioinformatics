#!/usr/bin/python

DELETE = 0
INSERT = 1
BACK = 2
MATCH = 3

INDEL_COST = 0
MATCH_COST = 1
HALF_MATCH = 0
MISMATCH = 0

def max_alignment(v, w, x):
	"""
	table = []
	for i in xrange(len(v)+1):
		v_table = []
		for j in xrange(len(w)+1):
			w_table = []
			for k in xrange(len(x)+1):
				w_table.append(0)
			v_table.append(w_table)
		table.append(v_table)
	print table
	"""
	table = [[[0 for _ in x+" "] for _ in w+" "] for _ in v+" "]
	ops = [[[0 for _ in x+" "] for _ in w+" "] for _ in v+" "]
	for i in xrange(len(v)+1):
		table[i][0][0] = INDEL_COST * i
		ops[i][0][0] = DELETE
	for j in xrange(len(w)+1):
		table[0][j][0] = INDEL_COST * j
		ops[0][j][0] = INSERT
	for k in xrange(len(x)+1):
		table[0][0][k] = INDEL_COST * k
		ops[0][0][k] = BACK
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			for k in xrange(1, len(x)+1):
				table[i][j][k], ops[i][j][k] = max_index([table[i-1][j][k] + INDEL_COST, \
									table[i][j-1][k] + INDEL_COST, \
									table[i][j][k-1] + INDEL_COST, \
									table[i-1][j-1][k-1] + match_cost(v[i-1], w[j-1], x[k-1])])
	print table[len(v)][len(w)][len(x)]
	unwind_ops(ops, v, w, x, len(v), len(w), len(x))

def unwind_ops(ops, v, w, x, i, j, k):
	new_v = []
	new_w = []
	new_x = []
	while i != 0 or j != 0 or k != 0:
		if i < 0 or j < 0 or k < 0:
			print "ERROR: index got too low: (i, j, k):", i, j, k
		if ops[i][j][k] == DELETE:
			new_v.append(v[i-1])
			i-=1
			new_w.append("-")
			new_x.append("-")
		elif ops[i][j][k] == INSERT:
			new_w.append(w[j-1])
			j-=1
			new_v.append("-")
			new_x.append("-")
		elif ops[i][j][k] == BACK:
			new_x.append(x[k-1])
			k-=1
			new_v.append("-")
			new_w.append("-")
		else:
			new_v.append(v[i-1])
			new_w.append(w[j-1])
			new_x.append(x[k-1])
			i-=1
			j-=1
			k-=1
		print ''.join(new_v[::-1])
		print ''.join(new_w[::-1])
		print ''.join(new_x[::-1])

def match_cost(p1, p2, p3):
	if p1 == p2 and p2 == p3:
		return MATCH_COST
	if p1 == p2 or p2 == p3:
		return HALF_MATCH
	return MISMATCH

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(1, len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

v, w, x = [line[:-1] for line in open("input.txt", "r")]
max_alignment(v, w, x)
