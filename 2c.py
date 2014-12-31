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
	return sorted(map(get_mass, get_subpeptides(peptide)))

def get_subpeptides(peptide):
	subs = [""]
	for length in xrange(1, len(peptide)):
		for i in xrange(len(peptide)):
			if i+length <= len(peptide):
				subs.append(peptide[i:i+length])
			else:
				rem = length - (len(peptide) - i)
				subs.append(peptide[i:] + peptide[0:rem])
	subs.append(peptide)
	return subs

def get_mass(subpeptide):
	return reduce(lambda x,y: x+y, map(lambda n: mass_table[n], list(subpeptide)), 0)

input = [line.split() for line in open("input.txt", "r")]
peptide = input[0][0]
print ' '.join(map(str, get_spectrum(peptide)))
