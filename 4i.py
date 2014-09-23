#!/usr/bin/python

def reconstruct(d, reads):
	pass

def paired_composition(k, d, text):
	composition = []
	for index in xrange(len(text) - (2 * k + d) + 1):
		composition.append(text[index:index+k] + "|" + text[index+k+d:index+k+k+d])
	return composition

k = 3
d = 1
text = "TAATGCCATGGGATGTT"
reads = paired_composition(k, d, text)
print sorted(reads)
