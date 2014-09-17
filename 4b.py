#!/usr/bin/python

patterns = sorted([line[:-1] for line in open("input.txt", "r")])
print '\n'.join([patterns[i] + " -> " + patterns[j] for i in xrange(len(patterns)) for j in xrange(len(patterns)) if i!=j and patterns[i][1:] == patterns[j][:-1]])
