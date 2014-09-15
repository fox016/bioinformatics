import sys
import random

def median_string(dna_list, k):
	best = {"pattern": "", "distance": float("inf")}
	for pattern in get_combinations(k):
		current_distance = sum_distance(pattern, dna_list)
		if current_distance < best['distance']:
			best['pattern'] = pattern
			best['distance'] = current_distance
			print best
	return best['pattern']

def sum_distance(pattern, dna_list):
	return sum(map(lambda text: hamming_distance(pattern, text), dna_list))

def hamming_distance(pattern, text):
	k = len(pattern)
	shortest_distance = float("inf")
	for index in xrange(len(text) - k + 1):
		kmer = text[index:index+k]
		distance = count_diff(kmer, pattern, shortest_distance)
		if distance < shortest_distance:
			shortest_distance = distance
	return shortest_distance

def count_diff(s1, s2, min_diff):
	count = 0
	for index in xrange(len(s1)):
		if s1[index] != s2[index]:
			count+=1
			if count >= min_diff:
				return count
	return count

def get_combinations(length):
	pools = ["ACTG"] * length
	result = [""]
	for pool in pools:
		result = [x+y for x in result for y in pool]
	return result

"""
def generate_genome(length):
	genome = ""
	for i in xrange(length):
		genome += random.choice("ACTG")
	return genome

dna_list = []
for i in xrange(10):
	dna_list.append(generate_genome(100))
k = 5
print '\n'.join(dna_list)
print k
print median_string(dna_list, k)
"""
