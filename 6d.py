#!/usr/bin/python

nucleotide_pair_map = {"A":"T", "T":"A", "C":"G", "G":"C"}

def get_complement(sequence):
	return ''.join(map(lambda x: nucleotide_pair_map[x], sequence)[::-1])

read = [line[:-1] for line in open("/Users/Admin/Downloads/rosalind_6d.txt", "r")]
k, s1, s2 = int(read[0]), read[1], read[2]

kmer1_map = {}
kmer2_map = {}

for start in xrange(len(s1) - k + 1):
	kmer1_map[s1[start:start+k]] = start
for start in xrange(len(s2) - k + 1):
	kmer2_map[s2[start:start+k]] = start

results = set()
for kmer in kmer1_map.keys():
	kmer_comp = get_complement(kmer)
	if kmer in kmer2_map:
		results.add((kmer1_map[kmer], kmer2_map[kmer]))
	if kmer_comp in kmer2_map:
		results.add((kmer1_map[kmer], kmer2_map[kmer_comp]))
for kmer in kmer2_map.keys():
	kmer_comp = get_complement(kmer)
	if kmer_comp in kmer1_map:
		results.add((kmer1_map[kmer_comp], kmer2_map[kmer]))
for result in results:
	print result
