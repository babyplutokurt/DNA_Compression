import sys
import time
import struct
import array

def write_ascii_values_to_file(input_string, offset):
    try:
        return array.array('i', [ord(char) - offset for char in input_string])
    except Exception as e:
        print(f"Error: {e}")


def write_bytearray_to_large_file(file_path, int_array):
    try:
        with open(file_path, 'ab') as file:
            byte_array = struct.pack('i' * len(int_array), *int_array)
            file.write(byte_array)
    except Exception as e:
        print(f"Error happen: {e}")


def retrieve(input_file, output_file_name_DNA, output_file_name_qualityScore, mode='1234'):
    try:
        count = 0
        DNA_Output = ''
        SCORE_Output = ''
        start_time = time.time()
        binFileName = output_file_name_qualityScore[:-4] + "_bin.bin"

        with open(input_file, "r") as fileobject, \
             open(output_file_name_DNA, 'a', encoding='utf-8') as dna_file, \
             open(output_file_name_qualityScore, 'a', encoding='utf-8') as score_file, \
             open(binFileName, 'ab') as bin_file:

            for line in fileobject:
                if line[0] != '@':
                    count += 1
                    if count > 5000000:
                        break
                    x = line.split()
                    DNA_Output = x[9]
                    dna_file.write(DNA_Output)
                    SCORE_Output = x[10]
                    score_file.write(SCORE_Output)
                    x = write_ascii_values_to_file(SCORE_Output, 31)
                    x.tofile(bin_file)

        assert len(DNA_Output) == len(
            SCORE_Output), f"String length unmatched, {output_file_name_DNA} length: {len(DNA_Output)}, " \
                           f"while {output_file_name_qualityScore} length: {len(SCORE_Output)}"

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        print(f"DNA content written to {output_file_name_DNA}")
        print(f"SCORE content written to {output_file_name_qualityScore}")
        print(f"Binary Score content written to {binFileName}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py input_file output_file_name_DNA output_file_name_qualityScore")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_file_name_DNA = sys.argv[2]
    output_file_name_qualityScore = sys.argv[3]
    retrieve(input_file_name, output_file_name_DNA, output_file_name_qualityScore)
