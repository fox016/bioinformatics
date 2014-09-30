#!/usr/bin/python

class Graph:

	def __init__(self):
		self.edges = set()
		self.node_edge_head_map = {}
		self.node_edge_tail_map = {}
		self.cycle = []
		self.start_nodes = set()
		self.extra_edge = None
	
	def add_edge(self, n1, n2):
		edge = (n1, n2)
		self.edges.add(edge)
		if n1 in self.node_edge_head_map:
			self.node_edge_head_map[n1].add(edge)
		else:
			self.node_edge_head_map[n1] = set([edge])
		if n2 in self.node_edge_tail_map:
			self.node_edge_tail_map[n2].add(edge)
		else:
			self.node_edge_tail_map[n2] = set([edge])

	def get_contigs(self):
		return map(self._get_contif_helper, self._get_branching_head_nodes())

	def _get_contig_helper(self, node):
		if not self._is_branching(node):
			return node
		return node #TODO

	def _get_branching_head_nodes(self):
		return filter(self._is_branching, self.node_edge_head_map.keys())

	def _is_branching(self, node):
		if node not in self.node_edge_head_map or node not in self.node_edge_tail_map:
			return True
		elif len(self.node_edge_head_map[node]) != 1 or len(self.node_edge_tail_map[node]) != 1:
			return True
		return False

edge_input = [line[:-1] for line in open("input.txt", "r")]
graph = Graph()
for e in edge_input:
	graph.add_edge(e[0:-1], e[1:])
print graph.get_contigs()
