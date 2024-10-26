import os
import sys

DEFAULT_HEADER_SIZE = 32

def display_header(byte_data):
    """
    Display file headers in a human readable format.

    Parameters:
    byte_data (list): File header in byte format

    Returns:
    None
	"""

    if not byte_data:
        print('No bytes found')
    else:
        hex_output = ' '.join(f'{byte:02x}' for byte in byte_data)
        ascii_output = ' '.join(f'{chr(byte):>2}' for byte in byte_data)
        print(f'hex   | {hex_output}')
        print(f'ascii | {ascii_output}')

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

        headers = {}

        # Loop through the files in the directory
        for filename in os.listdir(directory):
            # Check if the file ends with the specified extension
            if filename.endswith(extension):
                with open(os.path.join(directory, filename), 'rb') as file:
                    # Read the first few bytes
                    bytes_read = file.read(header_size)
                
                    # Convert to hexadecimal format
                    # display_header(bytes_read)
                    headers[bytes_read] = headers.get(bytes_read, 0) + 1

        # Display unique file headers
        if headers:
            # display header size for clarity
            print(f'Displaying the first {header_size} bytes')

            # display headers according to frequency
            keys = sorted(headers.keys(), key=lambda k: -headers[k])
            for key in keys:
                display_header(key)
        else:
            print("The directory was empty")

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