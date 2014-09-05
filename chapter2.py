import sys

nucleotide_pair_map = {"A":"T", "T":"A", "C":"G", "G":"C"}

def build_peptide(rna):
	codons = []
	for index in xrange(0, len(rna), 3):
		codons.append(rna[index:index+3])
	peptide = map(translate_codon, codons)
	return ''.join(peptide)

def find_peptide_encoding(genome, peptide):
	window_size = len(peptide)*3
	windows = []
	for index in xrange(len(genome) - window_size + 1):
		window = genome[index:index+window_size]
		if build_peptide(build_rna(window)) == peptide or build_peptide(build_rna(get_complement(window))) == peptide:
			windows.append(window)
	return windows

def build_rna(dna):
	return dna.replace("T","U")

def translate_codon(codon):
	codon = codon.lower()
	c1 = codon[0]
	c2 = codon[1]
	c3 = codon[2]
	if c1 == "a":
		if c2 == "a":
			if c3 == "a":
				return "K"
			elif c3 == "c":
				return "N"
			elif c3 == "g":
				return "K"
			else:
				return "N"
		elif c2 == "c":
			return "T"
		elif c2 == "g":
			if c3 == "a":
				return "R"
			elif c3 == "c":
				return "S"
			elif c3 == "g":
				return "R"
			else:
				return "S"
		else:
			if c3 == "a":
				return "I"
			elif c3 == "c":
				return "I"
			elif c3 == "g":
				return "M"
			else:
				return "I"
	elif c1 == "c":
		if c2 == "a":
			if c3 == "a":
				return "Q"
			elif c3 == "c":
				return "H"
			elif c3 == "g":
				return "Q"
			else:
				return "H"
		elif c2 == "c":
			return "P"
		elif c2 == "g":
			return "R"
		else:
			return "L"
	elif c1 == "g":
		if c2 == "a":
			if c3 == "a":
				return "E"
			elif c3 == "c":
				return "D"
			elif c3 == "g":
				return "E"
			else:
				return "D"
		elif c2 == "c":
			return "A"
		elif c2 == "g":
			return "G"
		else:
			return "V"
	else:
		if c2 == "a":
			if c3 == "a":
				return "*"
			elif c3 == "c":
				return "Y"
			elif c3 == "g":
				return "*"
			else:
				return "Y"
		elif c2 == "c":
			return "S"
		elif c2 == "g":
			if c3 == "a":
				return "*"
			elif c3 == "c":
				return "C"
			elif c3 == "g":
				return "W"
			else:
				return "C"
		else:
			if c3 == "a":
				return "L"
			elif c3 == "c":
				return "F"
			elif c3 == "g":
				return "L"
			else:
				return "F"
	return "ERR"

def get_complement(sequence):
	return ''.join(map(lambda x: nucleotide_pair_map[x], sequence)[::-1])

filename = sys.argv[1]
input = [line.split() for line in open(filename, "r")]
rna = input[0][0]
print build_peptide(rna)
