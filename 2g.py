def spectral_convolution(spectrum):
	spectrum = sorted(spectrum)
	element_freq_map = {}
	for high_index in xrange(1, len(spectrum)):
		for low_index in xrange(high_index):
			element = spectrum[high_index] - spectrum[low_index]
			if element == 0:
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
		for element in freq_element_map[freq]:
			convolution += [element] * freq
	return convolution

spectrum = [map(int, line.split()) for line in open("input.txt", "r")][0]
output = open("output.txt", "w+")
solution = ' '.join(map(str, spectral_convolution(spectrum)))
output.write(solution)
output.close()
