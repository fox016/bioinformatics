#!/usr/bin/python

text = [line[:-1] for line in open("input.txt", "r")][0]
M = sorted([text[start:] + text[:start] for start in xrange(len(text))])
print ''.join([m[-1] for m in M])
