#!/usr/bin/python

def median_string(dna_list, k):
	best = {"pattern": "", "distance": float("inf")}
	for pattern in get_combinations(k):
		current_distance = sum_distance(pattern, dna_list)
		if current_distance < best['distance']:
			best['pattern'] = pattern
			best['distance'] = current_distance
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

read = [line for line in open("input.txt", "r")]
k = int(read[0])
dna_list = read[1:]
print median_string(dna_list, k)
