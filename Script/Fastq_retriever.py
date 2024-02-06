import array
from collections import Counter

from Bio import SeqIO

input_file = "/Users/taolueyang/DNA_Compression/Fastq/Sorted_test_1000.fq"
counter = Counter()
binFileName = '/Users/taolueyang/DNA_Compression/Fastq/Sorted_test_1000.bin'
binFileName_char = '/Users/taolueyang/DNA_Compression/Fastq/Sample/9_Swamp_S2B_rbcLa_2019_minq7_char.bin'

with open(binFileName, 'ab') as bin_file:
    buffer = 50
    count = 0
    Quality_score_batch = []
    for record in SeqIO.parse(input_file, "fastq"):
        score = record.letter_annotations["phred_quality"]
        Quality_score_batch += score
        counter.update(score)
        count += 1

        if count % buffer == 0:
            Quality_score_float = array.array('f', [float(i) for i in Quality_score_batch])
            Quality_score_float.tofile(bin_file)
            Quality_score_batch = []

    Quality_score_float = array.array('f', [float(i) for i in Quality_score_batch])
    Quality_score_float.tofile(bin_file)
    Quality_score_batch = []

print(len(counter))
