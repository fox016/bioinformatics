import sys

values = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

def sequence_cyclopeptide(spectrum):
	spectrum_mass = sum(spectrum)
	queue = set([tuple([0])])
	while queue:
		queue = expand(queue)
		prune = set()
		for peptide in queue:
			if sum(peptide) == spectrum_mass:
				if get_spectrum(peptide) == spectrum:
					yield peptide
				prune.add(peptide)
			elif not is_consistent(peptide, spectrum):
				prune.add(peptide)
		queue -= prune

def expand(queue):
	newItems = []
	for peptide in queue:
		for value in values:
			newItems.append(peptide + tuple([value]))
	for item in newItems:
		queue.add(item)
	return queue

def is_consistent(peptide, spectrum):
	spec_copy = list(spectrum)
	pep_spectrum = get_spectrum(peptide) # Error is here, things are doubled and stuff
	for mass in pep_spectrum:
		print spec_copy, pep_spectrum, mass
		try:
			spec_copy.remove(mass)
		except ValueError:
			return False
	print peptide
	return True

def get_spectrum(peptide):
	return sorted(map(sum, get_subpeptides(peptide)))

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

spectrum = map(int, "0 113 128 186 241 299 314 427".split())
#print list(sequence_cyclopeptide(spectrum))
print is_consistent((0, 113, 128), (0, 113, 128, 128))
