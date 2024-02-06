import array
from collections import Counter
from Bio import SeqIO

fastq_file_path = '/Users/taolueyang/DNA_Compression/Fastq/Sample/9_Swamp_S2B_rbcLa_2019_minq7.fastq'
quality_scores_file_path = 'quality_scores.txt'

# Open the output file
with open(quality_scores_file_path, 'w') as output_file:
    # Use SeqIO.parse to read the FASTQ file
    for record in SeqIO.parse(fastq_file_path, "fastq"):
        # Each record's quality scores are available as a list in record.letter_annotations["phred_quality"]
        quality_scores = record.letter_annotations["phred_quality"]
        quality_scores = [chr(i) for i in quality_scores]

        # Convert the quality scores to a string (space-separated values in this example)
        quality_scores_str = ''.join(quality_scores)
        print(quality_scores_str)
        # Write the quality scores to the output file, with one record's scores per line
        output_file.write(quality_scores_str)

print(f"Quality scores have been written to {quality_scores_file_path}")