import sys

mass_table = {
	"G": 57,
	"A": 71,
	"S": 87,
	"P": 97,
	"V": 99,
	"T": 101,
	"C": 103,
	"I": 113,
	"L": 113,
	"N": 114,
	"D": 115,
	"K": 128,
	"Q": 128,
	"E": 129,
	"M": 131,
	"H": 137,
	"F": 147,
	"R": 156,
	"Y": 163,
	"W": 186
}

def get_spectrum(peptide):
	return map(get_mass, get_subpeptides(peptide))

def get_subpeptides(peptide):
	subs = [""]
	for length in xrange(1, len(peptide)+1):
		for i in xrange(len(peptide)):
			if i+length <= len(peptide):
				print i, i+length
				subs.append(peptide[i:i+length])
			else:
				have = len(peptide) - i
				rem = length - have
				print i, 0, rem-1
				subs.append(peptide[i:] + peptide[0:rem-1])
	subs.append(peptide)
	print subs
	return subs

def get_mass(subpeptide):
	return reduce(lambda x,y: x+y, map(lambda n: mass_table[n], list(subpeptide)), 0)

filename = sys.argv[1]
input = [line.split() for line in open(filename, "r")]
peptide = input[0][0]
print ' '.join(map(str, sorted(get_spectrum(peptide))))
