import os

# Function to calculate the length of the array stored in a binary file
def get_array_length(file_path):
    # Size of each integer in bytes (4 bytes for 'i' type)
    element_size = 4

    # Get the size of the file in bytes
    file_size = os.path.getsize(file_path)

    # Calculate the number of elements in the array
    num_elements = file_size // element_size
    return num_elements

# Path to the binary file
file_path = 'integers.bin'

# Calculate and print the length of the array
array_length = get_array_length("/Users/taolueyang/DNA_Compression/Output/SCORE_bin.bin")
print(f"The length of the array is: {array_length}")