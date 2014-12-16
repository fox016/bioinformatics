#!/usr/bin/python
import sys

nucleotide_value_map = {"A":1, "T":2, "C":3, "G":4}

def find_pattern(pattern, genome):
        tens_table = [pow(10, m) for m in xrange(len(pattern))]
        hash_pattern = get_hash(pattern, tens_table)
        index = []
        for current_index in xrange(len(genome) - len(pattern) + 1):
		if current_index == 0:
			current_hash = get_hash(genome[0:len(pattern)], tens_table)
		else:
			current_hash = ((current_hash - (nucleotide_value_map[genome[current_index-1]] * tens_table[len(pattern)-1])) * 10 + nucleotide_value_map[genome[current_index-1+len(pattern)]])
                if current_hash == hash_pattern:
                        index.append(current_index+1)
        return index

def get_hash(segment, tens_table):
        hash = 0
        for i in xrange(1, len(segment)+1):
                hash += (nucleotide_value_map[segment[i-1]] * tens_table[len(segment)-i])
        return hash

dna, pattern = [line[:-1] for line in open("input.txt", "r")]
print ' '.join(map(str, find_pattern(pattern, dna)))
