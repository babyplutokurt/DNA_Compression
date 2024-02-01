import array
import sys
import pysam


def write_ascii_values_to_file(input_string):
    return array.array('f', [int(ord(char)) - 33 for char in input_string])


def retrieve_cram(input_file_name = "HG00138_chr1.cram"):
    cram_file_path = input_file_name
    output_file_name_DNA = input_file_name[:-5] + "_DNA.txt"
    output_file_name_qualityScore = input_file_name[:-5] + "_SCORE.txt"
    quality_scores_string = ''
    buffer = 1000
    count = 0
    binFileName = output_file_name_qualityScore[:-4] + "_bin.bin"

    with pysam.AlignmentFile(cram_file_path, "rc") as cram_file, \
            open(output_file_name_DNA, 'a') as dna_file, \
            open(output_file_name_qualityScore, 'a') as score_file, \
            open(binFileName, 'ab') as bin_file:

        DNA_Output = ""
        SCORE_Output = ""
        Batch_size = 50
        Buffer_size = 200
        Plot_size = 10000
        minQuality = []
        quality_set = set([])

        for read in cram_file:
            # Convert the quality scores (which are integers) to characters
            quality_string = ''.join(chr(q + 33) for q in read.query_qualities)
            # quality_string = array.array('f', [float(char) for char in read.query_qualities])
            # print(len(quality_string))
            # quality_string = ''.join(chr(q + 33) for q in read.query_qualities)
            SCORE_Output += quality_string
            quality_set.update(quality_string)
            count += 1
            if count % buffer == 0:
                float_array = write_ascii_values_to_file(SCORE_Output)
                float_array.tofile(bin_file)
                print("Quality set length: ", len(quality_set))
                SCORE_Output = ''

        float_array = write_ascii_values_to_file(SCORE_Output)
        float_array.tofile(bin_file)
        print(len(quality_set))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py input_file output_file_name_DNA output_file_name_qualityScore")
        sys.exit(1)

    input_file_name = sys.argv[1]
    retrieve_cram(input_file_name)
