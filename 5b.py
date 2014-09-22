#!/usr/bin/python

def manhattan_tourist(n, m, down, right):
	s = []
	for i in xrange(n+1):
		s.append([0] * (m+1))
	for i in xrange(1, n+1):
		s[i][0] = s[i-1][0] + down[i-1][0]
	for j in xrange(1, m+1):
		s[0][j] = s[0][j-1] + right[0][j-1]
	for i in xrange(1, n+1):
		for j in xrange(1, m+1):
			s[i][j] = max(s[i-1][j] + down[i-1][j], s[i][j-1] + right[i][j-1])
	return s[n][m]

read = [line[:-1] for line in open("input.txt", "r")]
n, m = map(int, read[0].split())
down = map(lambda x: map(int, x.split()), read[1:read.index("-")])
right = map(lambda x: map(int, x.split()), read[read.index("-")+1:])
print manhattan_tourist(n, m, down, right)
