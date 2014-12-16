#!/usr/bin/python

alpha = "ACGT"
alpha_r = {"A": 0, "C": 1, "G": 2, "T": 3}

def get_consensus(profile):
	consensus = ""
	for j in xrange(len(profile[0])):
		best = (-1, "")
		for i in xrange(len(profile)):
			if profile[i][j] > best[0]:
				best = (profile[i][j], alpha[i])
		consensus += best[1]
	return consensus

def get_profile(dna_list):
	profile = [[0 for _ in dna_list[0]] for a in alpha]
	for dna in dna_list:
		for i in xrange(len(dna)):
			profile[alpha_r[dna[i]]][i]+=1
	return profile

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
profile = get_profile(dna_list)
consensus = get_consensus(profile)
print consensus
for i in xrange(len(profile)):
	print alpha[i] + ": " + ' '.join(map(str, profile[i]))
