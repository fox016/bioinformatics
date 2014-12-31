values = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

def sequence_cyclopeptide(spectrum):
	spectrum_mass = spectrum[-1]
	queue = set([tuple([0])])
	solution = []
	while queue:
		queue = expand(queue)
		prune = set()
		for peptide in queue:
			if sum(peptide) == spectrum_mass:
				if get_spectrum(peptide, True) == spectrum:
					solution.append(peptide)
				prune.add(peptide)
			elif not is_consistent(peptide, spectrum):
				prune.add(peptide)
		queue -= prune
		"""
		print queue
		raw_input()
		"""
	return solution

def expand(queue):
	return set([peptide + tuple([value]) for peptide in queue for value in values])

def is_consistent(peptide, spectrum):
	spec_copy = list(spectrum)
	pep_spectrum = get_spectrum(peptide, False)
	for mass in pep_spectrum:
		try:
			spec_copy.remove(mass)
		except ValueError:
			return False
	return True

def get_spectrum(peptide, isCircular):
	return sorted(map(sum, get_subpeptides(peptide, isCircular)))

def get_subpeptides(peptide, isCircular):
	if peptide[0] == 0:
		peptide = peptide[1:]
	subs = [(0,)]
	for length in xrange(1, len(peptide)):
		for i in xrange(len(peptide)):
			if i+length <= len(peptide):
				subs.append(peptide[i:i+length])
			elif isCircular:
				rem = length - (len(peptide) - i)
				subs.append(peptide[i:] + peptide[0:rem])
	subs.append(peptide)
	return subs

spectrum = [map(int, line.split()) for line in open("input.txt", "r")][0]
print ' '.join(map(lambda peptide: '-'.join(map(str, peptide[1:])), sequence_cyclopeptide(spectrum)))
