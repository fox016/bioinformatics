#!/usr/bin/python

def get_graph(kmers):
	graph = {}
	for i in xrange(len(kmers)):
		for j in xrange(len(kmers)):
			if kmers[i][1:] == kmers[j][:-1]:
				if kmers[i][:-1] not in graph:
					graph[kmers[i][:-1]] = set([kmers[j][:-1]])
				else:
					graph[kmers[i][:-1]].add(kmers[j][:-1])
				if kmers[i][1:] not in graph:
					graph[kmers[i][1:]] = set([kmers[j][1:]])
				else:
					graph[kmers[i][1:]].add(kmers[j][1:])
	return graph

def print_graph(graph):
	for key in sorted(graph.keys()):
		print key +  " -> " + ','.join(sorted(graph[key]))

kmers = [line[:-1] for line in open("input.txt", "r")]
print_graph(get_graph(kmers))
