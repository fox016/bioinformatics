#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2

EDIT_COST = -5

def max_alignment(v, w):
	table = []
	ops = []
	for i in xrange(len(v)+1):
		table.append([0] * (len(w)+1))
		ops.append([0] * (len(w)+1))
	for i in xrange(len(v)+1):
		table[i][0] = EDIT_COST * i
		ops[i][0] = DELETE
	for j in xrange(len(w)+1):
		table[0][j] = EDIT_COST * j
		ops[0][j] = INSERT
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			table[i][j], ops[i][j] = max_index([table[i-1][j] + EDIT_COST, \
					table[i][j-1] + EDIT_COST, \
					table[i-1][j-1] + match_cost(v[i-1], w[j-1])])
	return get_op_count(ops, v, w, len(v), len(w))

def get_op_count(ops, v, w, i, j):
	op_count = 0
	while i != 0 or j != 0:
		if ops[i][j] == DELETE:
			op_count+=1
			i-=1
		elif ops[i][j] == INSERT:
			op_count+=1
			j-=1
		else:
			if v[i-1] != w[j-1]:
				op_count+=1
			i-=1
			j-=1
	return op_count

def match_cost(p1, p2):
	return 0 if p1 == p2 else EDIT_COST

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(1, len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

v, w = [line[:-1] for line in open("input.txt", "r")]
print max_alignment(v, w)
