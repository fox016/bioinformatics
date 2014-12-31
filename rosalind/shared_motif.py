#!/usr/bin/python

def in_all_dna(sub, dna_list):
	for dna in dna_list:
		if sub not in dna:
			return False
	return True

def longest_common_sub(dna_list):
	base = min(dna_list, key=lambda x: len(x))
	for length in xrange(len(base), 0, -1):
		for index in xrange(0, len(base)-length+1):
			sub = base[index:index+length]
			if in_all_dna(sub, dna_list):
				return sub
	return None

def read_input():
	lines = [line[:-1] for line in open("input.txt")]
	dna_list = {}
	for line in lines:
		if line[0] == ">":
			current_name = line[1:]
			dna_list[current_name] = ""
		else:
			dna_list[current_name] += line
	return dna_list.values()

dna_list = read_input()
print longest_common_sub(dna_list)
