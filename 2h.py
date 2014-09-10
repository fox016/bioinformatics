import sys

def convolution_sequence_cyclopeptide(m, n, spectrum):
	spectrum_mass = spectrum[-1]
	leaderboard = set([tuple([0])])
	leaderPeptide = tuple([0])
	convolution = spectral_convolution(spectrum, m)
	while leaderboard:
		leaderboard = expand(leaderboard, convolution)
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

def expand(queue, convolution):
	return set([peptide + tuple([value]) for peptide in queue for value in convolution])

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
		cutboard.update(score_peptide_map[key])
		if len(cutboard) >= n:
			return cutboard
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

def spectral_convolution(spectrum, m):
	spectrum = sorted(spectrum)
	element_freq_map = {}
	for high_index in xrange(1, len(spectrum)):
		for low_index in xrange(high_index):
			element = spectrum[high_index] - spectrum[low_index]
			if element < 57 or element > 200:
				continue
			if element in element_freq_map:
				element_freq_map[element] += 1
			else:
				element_freq_map[element] = 1
	freq_element_map = {}
	for element in element_freq_map:
		freq = element_freq_map[element]
		if freq in freq_element_map:
			freq_element_map[freq].append(element)
		else:
			freq_element_map[freq] = [element]
	convolution = []
	for freq in reversed(sorted(freq_element_map.keys())):
		convolution += freq_element_map[freq]
		if len(convolution) >= m:
			return sorted(convolution)
	return sorted(convolution)

input = [map(int, line.split()) for line in open("input.txt", "r")]
m = input[0][0]
n = input[1][0]
spectrum = sorted(input[2])
print '-'.join(map(str, convolution_sequence_cyclopeptide(m, n, spectrum)[1:]))
