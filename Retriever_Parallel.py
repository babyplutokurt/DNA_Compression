import sys
import time
import struct
from concurrent.futures import ThreadPoolExecutor

def write_ascii_values_to_file(input_string, offset):
    try:
        return [ord(char) - offset for char in input_string]
    except Exception as e:
        print(f"Error: {e}")

def write_bytearray_to_large_file(file_path, int_array):
    try:
        with open(file_path, 'ab') as file:
            byte_array = struct.pack('i' * len(int_array), *int_array)
            file.write(byte_array)
    except Exception as e:
        print(f"Error happen: {e}")

def process_line(line, dna_file, score_file, bin_file):
    if line[0] != '@':
        x = line.split()
        DNA_Output = x[9]
        dna_file.write(DNA_Output)
        SCORE_Output = x[10]
        score_file.write(SCORE_Output)
        x = write_ascii_values_to_file(SCORE_Output, 31)
        bin_file.write(struct.pack('i' * len(x), *x))

def retrieve_parallel(input_file, output_file_name_DNA, output_file_name_qualityScore, mode='1234', num_threads=8):
    try:
        start_time = time.time()
        binFileName = output_file_name_qualityScore[:-4] + "_bin.bin"
        count = 0
        with open(input_file, "r") as fileobject, \
             open(output_file_name_DNA, 'a', encoding='utf-8') as dna_file, \
             open(output_file_name_qualityScore, 'a', encoding='utf-8') as score_file, \
             open(binFileName, 'ab') as bin_file:

            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for line in fileobject:
                    futures.append(executor.submit(process_line, line, dna_file, score_file, bin_file))
                    count += 1
                    if count > 5000000:
                        break

                print("Threads initialize done")

                # Wait for all threads to complete
                for future in futures:
                    future.result()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        print(f"DNA content written to {output_file_name_DNA}")
        print(f"SCORE content written to {output_file_name_qualityScore}")
        print(f"Binary Score content written to {binFileName}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python script_name.py input_file output_file_name_DNA output_file_name_qualityScore")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_file_name_DNA = sys.argv[2]
    output_file_name_qualityScore = sys.argv[3]
    retrieve_parallel(input_file_name, output_file_name_DNA, output_file_name_qualityScore)
