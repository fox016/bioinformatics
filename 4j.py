#!/usr/bin/python

import sys

class Graph:

	def __init__(self):
		self.node_edge_head_map = {}
		self.node_edge_tail_map = {}
		self.edges = set()
		self.edge_count_map = {}
	
	def add_edge(self, n1, n2):
		edge = (n1, n2)
		if edge in self.edges:
			self.edge_count_map[edge] += 1
			return
		self.edges.add(edge)
		self.edge_count_map[edge] = 1
		if n1 in self.node_edge_head_map:
			self.node_edge_head_map[n1].append(edge)
		else:
			self.node_edge_head_map[n1] = [edge]
		if n2 in self.node_edge_tail_map:
			self.node_edge_tail_map[n2].append(edge)
		else:
			self.node_edge_tail_map[n2] = [edge]

	def get_contigs(self):
		contigs = map(lambda node: self._get_contig_helper(node), self._get_branching_head_nodes())
		strings = []
		for list_of_list_of_strs in contigs:
			for list_of_strs in list_of_list_of_strs:
				strings.append(list_of_strs[0] + ''.join(map(lambda x: x[-1], list_of_strs[1:])))
		return strings

	def _get_contig_helper(self, node, path=[]):
		if self._is_branching(node) and len(path) > 0:
			return [path + [node]]
		paths = []
		for edge in self.node_edge_head_map[node]:
			next_node = edge[1]
			paths += self._get_contig_helper(next_node, path + [node])
		return paths

	def _get_branching_head_nodes(self):
		return filter(self._is_branching, self.node_edge_head_map.keys())

	def _is_branching(self, node):
		if node not in self.node_edge_head_map or node not in self.node_edge_tail_map:
			return True
		if len(self.node_edge_head_map[node]) != 1 or len(self.node_edge_tail_map[node]) != 1:
			return True
		return False

	def __str__(self):
		heads = []
		for head in self.node_edge_head_map.keys():
			edges = map(lambda x:x[1], self.node_edge_head_map[head])
			heads.append(head + "->" + ','.join(edges))
		return '\n'.join(heads)

def kmer_composition(text, k):
	return [text[i:i+k] for i in xrange(len(text)-k+1)]

filename = sys.argv[1]
k = int(sys.argv[2])
reads = [line[:-1] for line in open(filename, "r")]
graph = Graph()
for read in reads:
	if read[0] == ">":
		continue
	kmers = kmer_composition(read, k)
	for index in xrange(1, len(kmers)):
		graph.add_edge(kmers[index-1], kmers[index])
print '\n'.join(graph.get_contigs())

"""
print '\n----GRAPH----'
print graph
"""
