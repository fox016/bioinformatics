#!/usr/bin/python

import sys

class Graph:

	def __init__(self, threshold=1):
		self.node_edge_head_map = {}
		self.node_edge_tail_map = {}
		self.edges = set()
		self.edge_count_map = {}
		self.min_count_accepted = threshold
	
	def add_edge(self, n1, n2):
		edge = (n1, n2)
		if edge in self.edges:
			self.edge_count_map[edge] += 1
		else:
			self.edges.add(edge)
			self.edge_count_map[edge] = 1
		if self.edge_count_map[edge] == self.min_count_accepted: 
			if n1 in self.node_edge_head_map:
				self.node_edge_head_map[n1].append(edge)
			else:
				self.node_edge_head_map[n1] = [edge]
			if n2 in self.node_edge_tail_map:
				self.node_edge_tail_map[n2].append(edge)
			else:
				self.node_edge_tail_map[n2] = [edge]

	def get_contigs(self):
		contigs = []
		for node in self._get_branching_head_nodes():
			for edge in self.node_edge_head_map[node]:
				next_node = edge[1]
				contig = node
				while not self._is_branching(next_node):
					contig += next_node[-1]
					next_node = self.node_edge_head_map[next_node][0][1]
				contig += next_node[-1]
				contigs.append(contig)
		return contigs

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
threshold = int(sys.argv[3])
reads = [line[:-1] for line in open(filename, "r")]
graph = Graph(threshold)
for read in reads:
	if read[0] == ">":
		continue
	kmers = kmer_composition(read, k)
	for index in xrange(1, len(kmers)):
		graph.add_edge(kmers[index-1], kmers[index])
print ' '.join(graph.get_contigs())
