#!/usr/bin/python

class Graph:

	def __init__(self):
		self.edges = set()
		self.node_edge_map = dict()
		self.start_nodes = set()
	
	def add_edge(self, n1, n2):
		edge = (n1, n2)
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
			self.print_cycle(cycle)
		return cycle
	
	def print_cycle(self, cycle):
		output = cycle[0][0]
		for edge in cycle:
			output += "->" + edge[1]
		print output

	def _form_cycle(self, start):
		current = start
		current_cycle = []
		while True:
			edge = self.node_edge_map[current].pop()
			if len(self.node_edge_map[current]) == 0:
				self.start_nodes.discard(current)
			current_cycle.append(edge)
			self.edges.remove(edge)
			current = edge[1]
			if current == start:
				return current_cycle


edge_input = [line.split() for line in open("input.txt", "r")]
graph = Graph()
for e in edge_input:
	n1 = e[0]
	for n2 in e[2].split(','):
		graph.add_edge(n1, n2)
cycle = graph.eulerian_cycle()
#graph.print_cycle(cycle)
