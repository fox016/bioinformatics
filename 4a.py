#!/usr/bin/python

read = [line for line in open("input.txt", "r")]
k, text = int(read[0][:-1]), read[1][:-1]
print '\n'.join(sorted([text[i:i+k] for i in xrange(len(text) - k + 1)]))
