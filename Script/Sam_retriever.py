import array
import sys
import time
from collections import Counter

from matplotlib import pyplot as plt

transform_dic = {30: 8.0, 20: 7.0, 10: 6.0, 6: 5.0, 5: 4.0, 4: 3.0, 3: 2.0, 2: 1.0}


def write_ascii_values_to_file(input_string):
    return array.array('f', [transform_dic[int(ord(char)) - 33] for char in input_string])


def retrieve(input_file, output_file_name_DNA, output_file_name_qualityScore):
    start_time = time.time()
    binFileName = output_file_name_qualityScore[:-4] + "_bin.bin"
    count = 0

    with open(input_file, "r") as fileobject, \
            open(output_file_name_DNA, 'a') as dna_file, \
            open(output_file_name_qualityScore, 'a') as score_file, \
            open(binFileName, 'ab') as bin_file:

        DNA_Output = ""
        SCORE_Output = ""
        Batch_size = 50000
        Buffer_size = 1
        Plot_size = 10000
        counter = Counter([])
        minQuality = []

        for line in fileobject:
            if line[0] != '@':
                count += 1
                Batch_size += 1
                if count > 5000000:  # Limit to first 5 million records
                    break
                x = line.split()
                DNA_Output += x[9]
                SCORE_Output += x[10]
                counter.update(SCORE_Output)
                if count % Buffer_size == 0:
                    # dna_file.write(DNA_Output)
                    score_file.write(SCORE_Output)
                    # float_array = write_ascii_values_to_file(SCORE_Output)
                    # minQuality.append(min(float_array))
                    # counter.update(float_array)
                    # float_array.file(bin_file)
                    DNA_Output = ""
                    SCORE_Output = ""
                # print("Iter once!")
                if Batch_size % Plot_size == Plot_size + 1:
                    plt.figure(figsize=(20, 10))
                    plt.scatter(range(len(minQuality)), minQuality)  # 'o' is used to mark each point
                    plt.title('List Array Values')
                    plt.xlabel('Index')
                    plt.ylabel('Value')
                    plt.grid(False)
                    plt.show()
                    minQuality.clear()

    assert len(DNA_Output) == len(
        SCORE_Output), f"String length unmatched, {output_file_name_DNA} length: {len(DNA_Output)}, " \
                       f"while {output_file_name_qualityScore} length: {len(SCORE_Output)}"
    print(counter)
    print(len(counter))
    # dna_file.write(DNA_Output)
    score_file.write(SCORE_Output)
    # float_array = write_ascii_values_to_file(SCORE_Output)
    # counter.update(float_array)
    # float_array.tofile(bin_file)

    print(counter)

    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(f"DNA content written to {output_file_name_DNA}")
    print(f"SCORE content written to {output_file_name_qualityScore}")
    print(f"Binary Score content written to {binFileName}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py input_file output_file_name_DNA output_file_name_qualityScore")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_file_name_DNA = sys.argv[2]
    output_file_name_qualityScore = sys.argv[3]
    retrieve(input_file_name, output_file_name_DNA, output_file_name_qualityScore)
