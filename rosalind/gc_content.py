#!/usr/bin/python

def gc_content(dna):
	return 100 * (dna.count("C") + dna.count("G")) / float(len(dna))

def get_best_content(dna_list):
	best = (0, "")
	for name in dna_list:
		current_gc = gc_content(dna_list[name])
		if current_gc > best[0]:
			best = (current_gc, name)
	return best

def read_input():
	lines = [line[:-1] for line in open("input.txt")]
	dna = {}
	for line in lines:
		if line[0] == ">":
			current_name = line[1:]
			dna[current_name] = ""
		else:
			dna[current_name] += line
	return dna

dna_list = read_input()
best = get_best_content(dna_list)
print best[1]
print best[0]
