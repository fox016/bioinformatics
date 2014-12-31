#!/usr/bin/python

def get_adj_list(dna_list):
	adj_list = []
	for i in xrange(len(dna_list)):
		for j in xrange(len(dna_list)):
			if i == j:
				continue
			if dna_list[i][-3:] == dna_list[j][:3]:
				adj_list.append((dna_list[i],dna_list[j]))
	return adj_list

def read_input():
	lines = [line[:-1] for line in open("input.txt")]
	dna_map = {}
	current_val = ""
	for line in lines:
		if line[0] == ">":
			if current_val != "":
				dna_map[current_val] = current_name
			current_name = line[1:]
			current_val = ""
		else:
			current_val += line
	dna_map[current_val] = current_name
	return dna_map

dna_map = read_input()
adj_list = get_adj_list(dna_map.keys())
for adj in adj_list:
	print dna_map[adj[0]], dna_map[adj[1]]
