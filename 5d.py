#!/usr/bin/python

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

class Graph:

	def __init__(self, source, sink):
		self.source = source
		self.sink = sink
		self.node_score_map = {}
		self.node_back_map = {}
		self.node_edge_tail_map = {}
	
	def add_edge(self, head, tail, weight):
		edge = {"head": head, "tail": tail, "weight": weight}
		if tail not in self.node_edge_tail_map:
			self.node_edge_tail_map[tail] = [edge]
		else:
			self.node_edge_tail_map[tail].append(edge)
	
	def longest_path(self):
		self.node_score_map[self.source] = 0
		self.node_back_map[self.source] = None
		self._score_node(self.sink)

	def get_length(self):
		return self.node_score_map[self.sink]

	def get_path(self):
		path = []
		node = self.sink
		while node != None:
			path.append(node)
			node = self.node_back_map[node]
		return path[::-1]
	
	def _score_node(self, node):
		if node not in self.node_score_map:
			if node not in self.node_edge_tail_map:
				self.node_score_map[node] = float("-inf")
				self.node_back_map[node] = None
			else:
				predecessors = self.node_edge_tail_map[node]
				self.node_score_map[node], index = max_index(map(lambda edge: self._score_node(edge['head']) + edge['weight'], predecessors))
				self.node_back_map[node] = predecessors[index]["head"]
		return self.node_score_map[node]

read = [line[:-1] for line in open("input.txt", "r")]
source, sink = map(int, read[0:2])
graph = Graph(source, sink)
for edge in read[2:]:
	edge = edge.replace("->", ":")
	edge = map(int, edge.split(":"))
	graph.add_edge(edge[0], edge[1], edge[2])
graph.longest_path()
print graph.get_length()
print '->'.join(map(str, graph.get_path()))
