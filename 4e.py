#!/usr/bin/python

class Graph:

	def __init__(self):
		self.current_cycle = set()
		self.edges = set()
		self.node_edge_map = dict()
		self.start_nodes = set()
	
	def add_edge(self, n1, n2):
		edge = tuple(n1, n2)
		self.edges.add(edge)
		if n1 in self.node_edge_map:
			self.node_edge_map[n1].add(edge)
		else:
			self.node_edge_map[n1] = set([edge])
		self.start_nodes.add(n1)
	
	def eulerian_cycle(self):
		while self.edges:
			start = self.start_nodes.pop()
			cycle = self._form_cycle(start)
		return cycle

	def _form_cycle(start):
		pass #TODO

