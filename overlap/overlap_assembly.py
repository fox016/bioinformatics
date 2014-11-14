#!/usr/bin/python

import sys

DELETE, INSERT, MATCH, FREE = range(4)

MATCH_COST = 2
MISMATCH_COST = -1
INDEL_COST = -2

class Graph:

	def __init__(self):
		self.node_edge_head_map = {}
		self.node_tail_count = {}
	
	def add_edge(self, n1, n2):
		edge = (n1, n2)
		if n1 in self.node_edge_head_map:
			self.node_edge_head_map[n1].append(edge)
		else:
			self.node_edge_head_map[n1] = [edge]
		if n2 in self.node_tail_count:
			self.node_tail_count[n2] += 1
		else:
			self.node_tail_count[n2] = 1

	def get_contigs(self):
		contigs = []
		for node in self._get_branching_head_nodes():
			for edge in self.node_edge_head_map[node]:
				next_node = edge[1]
				contig = [node]
				while not self._is_branching(next_node):
					contig.append(next_node)
					next_node = self.node_edge_head_map[next_node][0][1]
				contig.append(next_node)
				contigs.append(contig)
		return contigs

	def _get_branching_head_nodes(self):
		return filter(self._is_branching, self.node_edge_head_map.keys())

	def _is_branching(self, node):
		if node not in self.node_edge_head_map or node not in self.node_tail_count:
			return True
		if len(self.node_edge_head_map[node]) != 1 or self.node_tail_count[node] != 1:
			return True
		return False

	def __str__(self):
		heads = []
		for head in self.node_edge_head_map.keys():
			edges = map(lambda x:x[1], self.node_edge_head_map[head])
			heads.append(head + "->" + ','.join(edges))
		return '\n'.join(heads)

def overlap_alignment(v, w, match_len):
	v = v[-1 * match_len:]
	w = w[0:match_len]
	table = [[0 for _ in w+" "] for _ in v+" "]
	ops = [[0 for _ in w+" "] for _ in v+" "]
	for i in xrange(len(v)+1):
		ops[i][0] = FREE
	for j in xrange(len(w)+1):
		table[0][j] = INDEL_COST * j
		ops[0][j] = INSERT
	for i in xrange(1, len(v)+1):
		for j in xrange(1, len(w)+1):
			table[i][j], ops[i][j] = max_index([table[i-1][j] + INDEL_COST, \
					table[i][j-1] + INDEL_COST, \
					table[i-1][j-1] + match_cost(v[i-1], w[j-1]), \
					table[0][j]])
	max_w, max_w_index = max_index([table[len(v)][index] for index in xrange(len(w)+1)])
	return unwind_ops(ops, v, w, len(v), max_w_index, table[len(v)][max_w_index])

def unwind_ops(ops, v, w, i, j, solution_cost):
	if solution_cost <= 0:
		return None
	new_v = []
	new_w = []
	v_len = 0
	w_len = 0
	while i != 0 or j != 0:
		if ops[i][j] == DELETE:
			new_v.append(v[i-1])
			v_len+=1
			i-=1
			new_w.append("-")
		elif ops[i][j] == INSERT:
			new_w.append(w[j-1])
			w_len+=1
			j-=1
			new_v.append("-")
		elif ops[i][j] == MATCH:
			new_v.append(v[i-1])
			new_w.append(w[j-1])
			v_len+=1
			w_len+=1
			i-=1
			j-=1
		else:
			i = 0
	v = ''.join(new_v[::-1])
	w = ''.join(new_w[::-1])
	overlap = ''
	for i in xrange(len(v)):
		if v[i] != '-':
			overlap += v[i]
		else:
			overlap += w[i]
	return {"overlap": overlap, "v_len": v_len, "w_len": w_len, "cost": solution_cost}

def match_cost(p1, p2):
	return MATCH_COST if p1 == p2 else MISMATCH_COST

def max_index(nums):
	best = (nums[0], 0)
	for index in xrange(1, len(nums)):
		if nums[index] > best[0]:
			best = (nums[index], index)
	return best

def rigid_overlap(v, w, match_len):
	for index in xrange(match_len):
		if v[len(v)-match_len+index] != w[index]:
			return False
	return True

def get_input_reads(filename):
	return [line[:-1] for line in open(filename, "r") if line[0] != ">"]

def build_graph(reads, match_len):
	matrix = [[None for _ in xrange(len(reads))] for _ in xrange(len(reads))]
	cost_coordinate_map = {}
	for i in xrange(len(reads)):
		for j in xrange(len(reads)):
			if i != j:
				entry = overlap_alignment(reads[i], reads[j], match_len)
				matrix[i][j] = entry
				if entry:
					if entry['cost'] in cost_coordinate_map:
						cost_coordinate_map[entry['cost']].append((i, j))
					else:
						cost_coordinate_map[entry['cost']] = [(i, j)]
	return matrix, cost_coordinate_map

def get_rigid_paths(reads, match_len):
	graph = Graph()
	for i in xrange(len(reads)):
		for j in xrange(len(reads)):
			if i != j:
				if rigid_overlap(reads[i], reads[j], match_len):
					graph.add_edge(i, j)
	return graph.get_contigs()

def get_rigid_contigs(paths, reads, overlap_len):
	contigs = []
	for path in paths:
		contig = reads[path[0]]
		for i in xrange(1, len(path)):
			node = path[i]
			contig += reads[node][overlap_len:]
		contigs.append(contig)
	return contigs

def reduce_matrix(matrix, cost_coordinate_map):
	row_overlap_map = {}
	for cost in sorted(cost_coordinate_map.keys(), reverse=True):
		for coor in cost_coordinate_map[cost]:
			if matrix[coor[0]][coor[1]]:
				if not path_exists(row_overlap_map, coor[1], coor[0]):
					row_overlap_map[coor[0]] = ({'row': coor[0],
								'col': coor[1],
								'overlap': matrix[coor[0]][coor[1]]['overlap'],
								'v_len': matrix[coor[0]][coor[1]]['v_len'],
								'w_len': matrix[coor[0]][coor[1]]['w_len']})
					for i in xrange(len(matrix)):
						matrix[coor[0]][i] = None
						matrix[i][coor[1]] = None
	return row_overlap_map

def path_exists(row_overlap_map, start, end):
	current = start
	while current in row_overlap_map:
		current = row_overlap_map[current]['col']
	return current == end

def build_contigs(reads, row_overlap_map):
	starts = set(row_overlap_map.keys())
	rows = set(row_overlap_map.keys())
	for row in rows:
		starts.discard(row_overlap_map[row]['col'])
	contigs = []
	for start in starts:
		contig = reads[row_overlap_map[start]['row']]
		current = start
		while current in rows:
			element = row_overlap_map[current]
			contig = contig[0:-1 * element['v_len']] + element['overlap'] + reads[element['col']][element['w_len']:]
			current = element['col']
		contigs.append(contig)
	return contigs

reads = get_input_reads(sys.argv[1])
match_len = int(sys.argv[2]) if len(sys.argv) > 2 else 10
rigid_method = True if len(sys.argv) > 3 else False

if not rigid_method:
	matrix, cost_coordinate_map = build_graph(reads, match_len)
	row_overlap_map = reduce_matrix(matrix, cost_coordinate_map)
	contigs = build_contigs(reads, row_overlap_map)
else:
	paths = get_rigid_paths(reads, match_len)
	contigs = get_rigid_contigs(paths, reads, match_len)

print '\n'.join(contigs)
