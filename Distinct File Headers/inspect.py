import os
import sys

DEFAULT_HEADER_SIZE = 32

def list_distinct_headers(directory, extension, header_size):
    """
    List all distinct headers found in files with a specific extension.

    Parameters:
    directory (str): The path to the directory to search.
    extension (str): The file extension to filter by (including the dot).
    header_size (int): The number of bytes to be considered

    Returns:
    None
    """
	
    try:
        # Ensure the directory exists
        if not os.path.isdir(directory):
            print(f"The directory '{directory}' does not exist.")
            return

        # Loop through the files in the directory
        for filename in os.listdir(directory):
            # Check if the file ends with the specified extension
            if filename.endswith(extension):
                # TODO extract header
                print(filename)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        # improper use case
        print("Usage: python inspect.py <directory> <file_extension> [<limit>]")
    else:
        # grab parameters and call script
        dir_path = sys.argv[1]
        file_ext = sys.argv[2]
        header_size = int(sys.argv[3]) if len(sys.argv) == 4 else DEFAULT_HEADER_SIZE
        list_distinct_headers(dir_path, file_ext, header_size)