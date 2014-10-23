#!/usr/bin/python

nucleotide_pair_map = {"A":"T", "T":"A", "C":"G", "G":"C"}
kmers = set()

def get_complement(sequence):
	return ''.join(map(lambda x: nucleotide_pair_map[x], sequence)[::-1])

def build_kmer_map(string, k):
	global kmers
	kmer_map = {}
	for start in xrange(len(string) - k + 1):
		kmer = string[start:start+k]
		kmers.add(kmer)
		if kmer not in kmer_map:
			kmer_map[kmer] = [start]
		else:
			kmer_map[kmer].append(start)
	return kmer_map

def get_pairs(first_list, last_list):
	return [(first, last) for first in first_list for last in last_list]

read = [line[:-1] for line in open("/Users/Admin/Downloads/rosalind_6d.txt", "r")]
k, s1, s2 = int(read[0]), read[1], read[2]
kmer1_map = build_kmer_map(s1, k)
kmer2_map = build_kmer_map(s2, k)

results = set()
for kmer in kmers:
	kmer_comp = get_complement(kmer)
	if kmer in kmer1_map:
		if kmer in kmer2_map:
			results.update(get_pairs(kmer1_map[kmer], kmer2_map[kmer]))
		elif kmer_comp in kmer2_map:
			results.update(get_pairs(kmer1_map[kmer], kmer2_map[kmer_comp]))
	if kmer_comp in kmer1_map:
		if kmer in kmer2_map:
			results.update(get_pairs(kmer1_map[kmer_comp], kmer2_map[kmer]))
		elif kmer_comp in kmer2_map:
			results.update(get_pairs(kmer1_map[kmer_comp], kmer2_map[kmer_comp]))
for result in results:
	print result
