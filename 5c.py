#!/usr/bin/python

DELETE = 0
INSERT = 1
MATCH = 2

def lcs(v, w):
	s = []
	ops = []
	for i in xrange(len(v)+1):
		s.append([0] * (len(w)+1))
		ops.append([0] * (len(w)+1))
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			if v[i-1] == w[j-1]:
				s[i][j], ops[i][j] = max_index([s[i-1][j], s[i][j-1], s[i-1][j-1]+1])
			else:
				s[i][j], ops[i][j] = max_index([s[i-1][j], s[i][j-1]])
	return ops

def lcs_unwind(ops, v, i, j):
	chars = []
	while i != 0 and j != 0:
		if ops[i][j] == DELETE:
			i-=1
		elif ops[i][j] == INSERT:
			j-=1
		else:
			chars.append(v[i-1])
			i-=1
			j-=1
	return chars[::-1]

def max_index(nums):
	best = (0, 0)
	for index in xrange(len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

read = [line[:-1] for line in open("input.txt", "r")]
ops = lcs(read[0], read[1])
print ''.join(lcs_unwind(ops, read[0], len(read[0]), len(read[1])))
