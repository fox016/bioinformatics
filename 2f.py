import sys

values = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

def leaderboard_sequence_cyclopeptide(spectrum, n):
	spectrum_mass = spectrum[-1]
	leaderboard = set([tuple([0])])
	leaderPeptide = tuple([0])
	while leaderboard:
		leaderboard = expand(leaderboard)
		prune = set()
		for peptide in leaderboard:
			if sum(peptide) == spectrum_mass:
				if score(peptide, spectrum) > score(leaderPeptide, spectrum):
					leaderPeptide = peptide
			elif not sum(peptide) > spectrum_mass:
				prune.add(peptide)
		leaderboard -= prune
		leaderboard = cut(leaderboard, spectrum, n)
	return leaderPeptide

def expand(queue):
	return set([peptide + tuple([value]) for peptide in queue for value in values])

def score(peptide, spectrum):
	spec_copy = list(spectrum)
	pep_spectrum = get_spectrum(peptide)
	misses = 0
	for mass in pep_spectrum:
		try:
			spec_copy.remove(mass)
		except ValueError:
			misses+=1
	return len(pep_spectrum) - misses

def cut(leaderboard, spectrum, n):
	pass # TODO

def get_spectrum(peptide):
	return sorted(map(sum, get_subpeptides(peptide)))

def get_subpeptides(peptide):
	if peptide[0] == 0:
		peptide = peptide[1:]
	subs = [(0,)]
	for length in xrange(1, len(peptide)):
		for i in xrange(len(peptide)):
			if i+length <= len(peptide):
				subs.append(peptide[i:i+length])
			"""
			else: # TODO I took this branch out and that seemed to make the example on page 60 run better
				rem = length - (len(peptide) - i)
				subs.append(peptide[i:] + peptide[0:rem])
			"""
	subs.append(peptide)
	return subs

input = [map(int, line.split()) for line in open("input.txt", "r")]
n = input[0][0]
spectrum = input[1]
print leaderboard_sequence_cyclopeptide(spectrum, n)
