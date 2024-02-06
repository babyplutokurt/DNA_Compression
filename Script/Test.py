strings = ["000000", "010101", "101010", "110110"]  # your set of strings
def hamming_distance(string1, string2):
    if len(string1) != len(string2):
        raise ValueError("Strings must be of the same length")
    return sum(c1 != c2 for c1, c2 in zip(string1, string2))


pairwise_distances = {}
for i, str1 in enumerate(strings):
    for j, str2 in enumerate(strings):
        if i < j:  # this ensures that each pair is only compared once
            distance = hamming_distance(str1, str2)
            pairwise_distances[(str1, str2)] = distance

print(pairwise_distances)