import numpy as np
from Bio import SeqIO

input_file1 = "/Users/taolueyang/DNA_Compression/Fastq/Sorted_test_1000.fq"
input_file2 = "/Users/taolueyang/DNA_Compression/Fastq/Sorted_test_1000_fastore_reduced.fastq"

def PSNR(y_true, y_pred):
    max_pixel = np.max(y_true)
    print(max_pixel)
    mse_value = np.mean((np_1 - np_2) ** 2)
    if mse_value == 0:
        # Means the two images are identical; PSNR has no meaning.
        return float('inf')
    return 20 * np.log10(max_pixel / np.sqrt(mse_value))


quality_score1 = []
fasta_id1 = []
fasta_seq1 = []
fasta_id2 = []
fasta_seq2 = []

for record in SeqIO.parse(input_file1, "fastq"):
    score = record.letter_annotations["phred_quality"]
    quality_score1.append(score)
    # fasta_seq.append(record.seq)
    fasta_id1.append(record.id)

quality_score2 = []
for record in SeqIO.parse(input_file2, "fastq"):
    score = record.letter_annotations["phred_quality"]
    quality_score2.append(score)
    fasta_id2.append(record.id)

np_1 = np.array(quality_score1)
np_2 = np.array(quality_score2)

fasta_id1_set = set(fasta_id1)
fasta_id2_set = set(fasta_id2)
difference = fasta_id1_set - fasta_id2_set
print(difference)

print(np_1.shape)
print(np_2.shape)
assert np_1.shape == np_2.shape, "two fastq file must have same shape"
mse = np.mean((np_1 - np_2) ** 2)
print("Mean Squared Error:", mse)

psnr_value = PSNR(np_1, np_2)
print(f"PSNR: {psnr_value} dB")
