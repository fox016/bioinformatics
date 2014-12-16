#!/usr/bin/python

def hamming(s, t):
	count = 0
	for i in xrange(len(s)):
		if s[i] != t[i]:
			count+=1
	return count

s, t = [line[:-1] for line in open("input.txt", "r")]
print hamming(s, t)
