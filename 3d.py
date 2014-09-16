#!/usr/bin/python

val_index_map = {"A": 0, "C": 1, "G": 2, "T": 3}

def greedy_motif_search(dna_list, k, t):
	best = {'motifs': [], 'score': 0}
	best['motifs'] = map(lambda dna: dna[0:k], dna_list)
	best['score'] = score(best['motifs'])
	for index in xrange(len(dna_list[0]) - k + 1):
		motifs = [""] * t
		motifs[0] = dna_list[0][index:index+k]
		for i in xrange(2, t+1):
			profile = get_profile(motifs[0:i-1])
			motifs[i-1] = profile_most_probable_kmer(dna_list[i-1], k, profile)
		current_score = score(motifs)
		if current_score < best['score']:
			best['motifs'] = motifs
			best['score'] = current_score
	return best['motifs']

def get_profile(motifs):
	k = len(motifs[0])
	profile = [[0] * k, [0] * k, [0] * k, [0] * k]
	for index in xrange(k):
		for column in map(lambda motif: motif[index], motifs):
			for value in column:
				profile[val_index_map[value]][index] += 1
	for row in xrange(4):
		for col in xrange(k):
			profile[row][col] /= float(len(motifs))
	return profile

def score(motifs):
	consensus = get_consensus(motifs)
	return sum(map(lambda motif: count_diff(motif, consensus), motifs))

def get_consensus(motifs):
	consensus = ""
	for index in xrange(len(motifs[0])):
		consensus += get_max(map(lambda motif: motif[index], motifs))
	return consensus

def get_max(column):
	counts = [0] * 4
	best = {'value': 'A', 'count': 0}
	for value in column:
		counts[val_index_map[value]]+=1
		if(counts[val_index_map[value]] > best['count']):
			best = {'value': value, 'count': counts[val_index_map[value]]}
	return best['value']

def count_diff(s1, s2):
	count = 0
	for index in xrange(len(s1)):
		if s1[index] != s2[index]:
			count+=1
	return count

def profile_most_probable_kmer(text, k, profile):
	best = {"kmer": "", "prob": -1}
	for index in xrange(len(text) - k + 1):
		kmer = text[index:index+k]
		prob = get_probability(kmer, profile)
		if prob > best['prob']:
			best['kmer'] = kmer
			best['prob'] = prob
	return best['kmer']

def get_probability(kmer, profile):
	return reduce(lambda x, y: x * y, map(lambda index: profile[val_index_map[kmer[index]]][index], xrange(len(kmer))), 1)

read = [line for line in open("input.txt", "r")]
k, t = map(int, read[0].split())
dna_list = map(lambda s: s[:-1], read[1:])
print '\n'.join(greedy_motif_search(dna_list, k, t))
