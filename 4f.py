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

	def eulerian_path(self):
		self._path_to_cycle()
		cycle = self.eulerian_cycle()
		for i in xrange(len(cycle)-1):
			edge = tuple(cycle[i:i+2])
			if edge == self.extra_edge:
				return cycle[i+1:] + cycle[1:i+1]
		return cycle

	def eulerian_cycle(self):
		while self.edges:
			start = self.start_nodes.pop()
			self._form_cycle(start)
		return self.cycle

	def _path_to_cycle(self):
		head, tail = None, None
		for key in self.node_edge_head_map.keys() + self.node_edge_tail_map.keys():
			if key not in self.node_edge_head_map:
				head = key
			elif key not in self.node_edge_tail_map:
				tail = key
			elif len(self.node_edge_tail_map[key]) < len(self.node_edge_head_map[key]):
				tail = key
			elif len(self.node_edge_tail_map[key]) > len(self.node_edge_head_map[key]):
				head = key
			if head and tail:
				break
		self.extra_edge = (head, tail)
		self.add_edge(head, tail)
		self.start_nodes.add(tail)

	def _form_cycle(self, start):
		current = start
		current_cycle = [start]
		while True:
			edge = self.node_edge_head_map[current].pop()
			if len(self.node_edge_head_map[current]) == 0:
				self.start_nodes.discard(current)
			else:
				self.start_nodes.add(current)
			current_cycle.append(edge[1])
			self.edges.remove(edge)
			current = edge[1]
			if current == start:
				if self.cycle:
					self.cycle = self.cycle[0:self.cycle.index(start)] + current_cycle + self.cycle[self.cycle.index(start)+1:]
				else:
					self.cycle = list(current_cycle)
				return

edge_input = [line.split() for line in open("input.txt", "r")]
graph = Graph()
for e in edge_input:
	n1 = e[0]
	for n2 in e[2].split(','):
		graph.add_edge(n1, n2)
print '->'.join(graph.eulerian_path())
