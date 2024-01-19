def write_ascii_values_to_file(input_string, offset):
    print(input_string)
    try:
        ascii_values = [ord(char) - offset for char in input_string]
        print("SSSSSSS")
        return ascii_values
    except Exception as e:
        print(f"Error: {e}")


print(write_ascii_values_to_file(
    "########################C=7@==8=2-5FEFFFEEEDEEFDECEDEEEDEE?CEEFEEDEFEEEEEFEEEFDEEDEDDCDECD@@", 31))
