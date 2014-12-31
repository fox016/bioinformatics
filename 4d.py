#!/usr/bin/python

def get_graph(kmers):
	graph = {}
	for kmer in kmers:
		if kmer[:-1] not in graph:
			graph[kmer[:-1]] = [kmer[1:]]
		else:
			graph[kmer[:-1]].append(kmer[1:])
	return graph

def print_graph(graph):
	for key in sorted(graph.keys()):
		print key +  " -> " + ','.join(sorted(graph[key]))

kmers = [line[:-1] for line in open("input.txt", "r")]
print_graph(get_graph(kmers))
