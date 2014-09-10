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
			elif sum(peptide) > spectrum_mass:
				prune.add(peptide)
		leaderboard -= prune
		leaderboard = cut(leaderboard, spectrum, n)
	return leaderPeptide

def expand(queue):
	return set([peptide + tuple([value]) for peptide in queue for value in values])

def score(peptide, spectrum):
	experimental = list(spectrum)
	theoretical = get_spectrum(peptide, True)
	misses = 0
	for mass in theoretical:
		try:
			experimental.remove(mass)
		except ValueError:
			misses+=1
	return len(theoretical) - misses

def cut(leaderboard, spectrum, n):
	score_peptide_map = {}
	for peptide in leaderboard:
		current_score = score(peptide, spectrum)
		if current_score not in score_peptide_map:
			score_peptide_map[current_score] = [peptide]
		else:
			score_peptide_map[current_score].append(peptide)
	cutboard = set()
	for key in reversed(sorted(score_peptide_map.keys())):
		if len(cutboard) >= n:
			return cutboard
		cutboard.update(score_peptide_map[key])
	return cutboard

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

input = [map(int, line.split()) for line in open("input.txt", "r")]
n = input[0][0]
spectrum = input[1]
print '-'.join(map(str, leaderboard_sequence_cyclopeptide(spectrum, n)[1:]))
