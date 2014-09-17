#!/usr/bin/python
import random

val_index_map = {"A": 0, "C": 1, "G": 2, "T": 3}

def gibbs_sampler(k, t, n, dna_list):
	motifs = get_random_motifs(dna_list, k)
	best = {'score': 0, 'motifs': motifs}
	best['score'] = score(best['motifs'])
	for j in xrange(n):
		i = random.randint(0, t-1)
		profile = get_profile((motifs[0:i] + motifs[i+1:]) if i+1 < t else motifs[0:i])
		motifs[i] = get_motif(profile, dna_list[i], k)
		current_score = score(motifs)
		if current_score < best['score']:
			best = {'score': current_score, 'motifs': motifs}
			print best
	return best['motifs']

def get_random_motifs(dna_list, k):
	motifs = []
	for dna in dna_list:
		index = random.randint(0, len(dna)-k)
		motifs.append(dna[index:index+k])
	return motifs

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

def get_profile(motifs):
	k = len(motifs[0])
	profile = [[1] * k, [1] * k, [1] * k, [1] * k]
	for index in xrange(k):
		for column in map(lambda motif: motif[index], motifs):
			for value in column:
				profile[val_index_map[value]][index] += 1
	for row in xrange(4):
		for col in xrange(k):
			profile[row][col] /= float(len(motifs)*2)
	return profile

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

def get_motif(profile, dna, k):
	return profile_most_probable_kmer(dna, k, profile) # TODO this is not how it is supposed to be done (see pages 113-114)

read = [line for line in open("input.txt", "r")]
k, t, n = map(int, read[0].split())
dna_list = map(lambda s: s[:-1], read[1:])

best = {'score': float("inf"), 'motifs': []}
for i in xrange(20):
	r = gibbs_sampler(k, t, n, dna_list)
	r_score = score(r)
	if r_score < best['score']:
		best = {'score': r_score, 'motifs': r}
print '\n'.join(best['motifs'])
