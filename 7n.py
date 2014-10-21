#!/usr/bin/python

nucleotide_value_map = {"A":1, "T":2, "C":3, "G":4}

def find_pattern(patterns, genome):
        tens_table = [pow(10, m) for m in xrange(len(patterns[0]))]
        hash_patterns = get_hashes(patterns, tens_table)
        index = []
        for current_index in xrange(len(genome) - len(patterns[0]) + 1):
		if current_index == 0:
			current_hash = get_hash(genome[0:len(patterns[0])], tens_table)
		else:
			current_hash = ((current_hash - (nucleotide_value_map[genome[current_index-1]] * tens_table[len(patterns[0])-1])) * 10 + nucleotide_value_map[genome[current_index-1+len(patterns[0])]])
                if current_hash in hash_patterns:
                        index.append(current_index)
        return index

def get_hash(segment, tens_table):
	hashcode = 0
	for i in xrange(1, len(segment)+1):
		hashcode += (nucleotide_value_map[segment[i-1]] * tens_table[len(segment)-i])
	return hashcode

def get_hashes(patterns, tens_table):
	hashes = set()	
	for segment in patterns:
		hashcode = 0
		for i in xrange(1, len(segment)+1):
			hashcode += (nucleotide_value_map[segment[i-1]] * tens_table[len(segment)-i])
		hashes.add(hashcode)
        return hashes

read = [line[:-1] for line in open("/Users/Admin/Downloads/rosalind_7n.txt", "r")]
genome = read[0]
patterns = read[1:]
print ' '.join(map(str, find_pattern(patterns, genome)))
