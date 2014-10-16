#!/usr/bin/python

def get_suffixes(text):
	suffix_index_map = {}
	for i in xrange(len(text)):
		suffix_index_map[text[i:]] = i
	return suffix_index_map

def suffix_array(text):
	suffixes = get_suffixes(text)
	keys = sorted(suffixes)
	return map(lambda key: suffixes[key], keys)

text = [line[:-1] for line in open("input.txt", "r")][0]
print ', '.join(map(str, suffix_array(text)))
