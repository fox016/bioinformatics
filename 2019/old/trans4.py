# n - number of times sequence should appear
# l - expected length of string

import sys

# Get all substrings of genome, length from min_len to max_len
# Map substring value to string index (1-based index)
def get_substrs(genome, min_len, max_len):
	substrs = {}
	for length in range(min_len, max_len+1):
		for start_pos in range(len(genome)-length+1):
			substr = genome[start_pos:start_pos+length]
			if substr in substrs:
				substrs[substr].append(start_pos+1)
			else:
				substrs[substr] = [start_pos+1]
	return substrs

# Find a kmer of length l that has n matches with up to 1 error in genome
def find_matches(n, l, genome):

	kmer_pos_map = {}
	alpha = "ACGT"
	
	# Get all INSERTS
	length = l-1
	for start_pos in range(len(genome)-length+1):
		substr = genome[start_pos:start_pos+length]
		for char in alpha:
			kmer = char + substr
			if kmer in kmer_pos_map:
				kmer_pos_map[kmer].add(start_pos+1)
			else:
				kmer_pos_map[kmer] = set()
				kmer_pos_map[kmer].add(start_pos+1)
			for i in range(len(substr)):
				kmer = substr[:i] + char + substr[i:]
				if kmer in kmer_pos_map:
					kmer_pos_map[kmer].add(start_pos+1)
				else:
					kmer_pos_map[kmer] = set()
					kmer_pos_map[kmer].add(start_pos+1)

	# Get all DELETES
	length = l+1
	for start_pos in range(len(genome)-length+1):
		substr = genome[start_pos:start_pos+length]
		for i in range(len(substr)):
			kmer = substr[:i]+substr[i+1:]
			if kmer in kmer_pos_map:
				kmer_pos_map[kmer].add(start_pos+1)
			else:
				kmer_pos_map[kmer] = set()
				kmer_pos_map[kmer].add(start_pos+1)

	# Get all MISMATCHES (including perfect matches)
	length = l
	for start_pos in range(len(genome)-length+1):
		substr = genome[start_pos:start_pos+length]
		if substr in kmer_pos_map:
			kmer_pos_map[substr].add(start_pos+1)
		else:
			kmer_pos_map[substr] = set()
			kmer_pos_map[substr].add(start_pos+1)
		for char in alpha:
			kmer = substr[:i] + char + substr[i+1:]
			if kmer in kmer_pos_map:
				kmer_pos_map[kmer].add(start_pos+1)
			else:
				kmer_pos_map[kmer] = set()
				kmer_pos_map[kmer].add(start_pos+1)
			
	# Find all kmers where kmer_pos_map[kmer] has length >= n
	kmers = list(filter(lambda kmer: len(kmer_pos_map[kmer]) >= n, kmer_pos_map))
	print kmers

	# Find ones that don't overlap
	for kmer in kmers:
		pos = kmer_pos_map[kmer]
		print kmer, pos

# Main
if __name__ == "__main__":
	infile = open("trans_in3.txt", "r")
	inputs = map(int, infile.readline().rstrip().split(" "))
	genome = infile.readline().rstrip()
	find_matches(inputs[0], inputs[1], genome)
