import os

def get_array_length(file_path):
    # Size of each float in bytes (4 bytes for a standard 32-bit float)
    float_size = 4

    # Get the size of the file in bytes
    file_size = os.path.getsize(file_path)

    # Calculate the number of floats in the file
    num_floats = file_size // float_size

    return num_floats

# Replace 'your_file.bin' with the path to your binary file
file_path = '/Users/taolueyang/DNA_Compression/Fastq/Sorted_test_1000.bin'
length = get_array_length(file_path)
print(f"The array contains {length} floats.")
