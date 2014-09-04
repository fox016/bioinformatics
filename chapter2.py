from chapter1 import get_complement

"""
-------------------- Global Variables
"""

"""
-------------------- Primary Functions
"""

def build_peptide(rna):
	codons = []
	for index in xrange(0, len(rna), 3):
		codons.append(rna[index:index+3])
	peptide = map(translate_codon, codons)
	return ''.join(peptide)

def find_peptide_encoding(genome, peptide):
	rna1 = build_rna(genome)
	rna2 = build_rna(get_complement(genome))
	translated_peptides = []
	translated_peptides.append(build_peptide(rna1))
	translated_peptides.append(build_peptide(rna1[1:] + rna1[0:1]))
	translated_peptides.append(build_peptide(rna1[2:] + rna1[0:2]))
	translated_peptides.append(build_peptide(rna2))
	translated_peptides.append(build_peptide(rna2[1:] + rna2[0:1]))
	translated_peptides.append(build_peptide(rna2[2:] + rna2[0:2]))
	return translated_peptides
	# TODO

"""
-------------------- Helper Functions
"""

def build_rna(dna):
	return dna.replace("T","U")

def translate_codon(codon):
	c1 = codon[0]
	c2 = codon[1]
	c3 = codon[2]
	if c1 == "a":
		if c2 == "a":
			if c3 == "a":
				return "Lys"
			elif c3 == "c":
				return "Asn"
			elif c3 == "g":
				return "Lys"
			else:
				return "Asn"
		elif c2 == "c":
			return "Thr"
		elif c2 == "g":
			if c3 == "a":
				return "Arg"
			elif c3 == "c":
				return "Ser"
			elif c3 == "g":
				return "Arg"
			else:
				return "Ser"
		else:
			if c3 == "a":
				return "Ile"
			elif c3 == "c":
				return "Ile"
			elif c3 == "g":
				return "Met"
			else:
				return "Ile"
	elif c1 == "c":
		if c2 == "a":
			if c3 == "a":
				return "Gln"
			elif c3 == "c":
				return "His"
			elif c3 == "g":
				return "Gln"
			else:
				return "His"
		elif c2 == "c":
			return "Pro"
		elif c2 == "g":
			return "Arg"
		else:
			return "Leu"
	elif c1 == "g":
		if c2 == "a":
			if c3 == "a":
				return "Glu"
			elif c3 == "c":
				return "Asp"
			elif c3 == "g":
				return "Glu"
			else:
				return "Asp"
		elif c2 == "c":
			return "Ala"
		elif c2 == "g":
			return "Gly"
		else:
			return "Val"
	else:
		if c2 == "a":
			if c3 == "a":
				return "XXX"
			elif c3 == "c":
				return "Tyr"
			elif c3 == "g":
				return "XXX"
			else:
				return "Tyr"
		elif c2 == "c":
			return "Ser"
		elif c2 == "g":
			if c3 == "a":
				return "XXX"
			elif c3 == "c":
				return "Cys"
			elif c3 == "g":
				return "Trp"
			else:
				return "Cys"
		else:
			if c3 == "a":
				return "Leu"
			elif c3 == "c":
				return "Phe"
			elif c3 == "g":
				return "Leu"
			else:
				return "Phe"
	return "ERR"

"""
-------------------- Script
"""

cholera = "atcaatgatcaacgtaagcttctaagcatgatcaaggtgctcacacagtttatccacaacctgagtggatgacatcaagataggtcgttgtatctccttcctctcgtactctcatgaccacggaaagatgatcaagagaggatgatttcttggccatatcgcaatgaatacttgtgacttgtgcttccaattgacatcttcagcgccatattgcgctggccaaggtgacggagcgggattacgaaagcatgatcatggctgttgttctgtttatcttgttttgactgagacttgttaggatagacggtttttcatcactgactagccaaagccttactctgcctgacatgcaccgtaaattgataatgaatttacatgcttccgcgacgatttacctcttgatcatcgatccgattgaagatcttcaattgttaattctcttgcctcgactcatagccatgatgagctcttgatcatgtttccttaaccctctattttttacggaagaatgatcaagctgctgctcttgatcatcgtttc"

print build_peptide(build_rna(cholera))

print find_peptide_encoding(cholera, "IleAsnAspGlnArgLysLeuLeuSer")
