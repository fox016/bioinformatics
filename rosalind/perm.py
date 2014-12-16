#!/usr/bin/python

from itertools import permutations

n = 6
perms = list(permutations(xrange(1,n+1)))
print len(perms)
for perm in perms:
	print ' '.join(map(str, perm))
