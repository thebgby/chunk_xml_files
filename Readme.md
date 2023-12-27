# XML File Chunking

## Overview

This Python script provides a simple utility for chunking XML files. It takes an input folder containing XML files, divides each XML file into chunks of a specified size, and saves the resulting chunks to an output folder. The chunking is based on the number of elements in the XML file.

## Requirements

- Python 3.x
- xml.etree.ElementTree module

## Usage

1. **Clone or download the repository to your local machine.**
2. **Ensure you have Python installed on your system.**
3. **Modify the script's configuration in the `if __name__ == "__main__":` block:**
   - `input_folder`: Path to the folder containing XML files.
   - `output_folder`: Path to the folder where the XML chunks will be saved.
   - `chunk_size`: Number of elements per chunk.
4. **Run the script.**

## Example

Suppose you have an input XML file named `example.xml` with 50 elements, and you want to create chunks of 10 elements each.

### Before Running the Script

- Input XML file: `example.xml` with 50 elements
- Output folder: `output_folder`

### After Running the Script

The output folder will contain five XML files:

- `example_chunk1.xml` (elements 1-10)
- `example_chunk2.xml` (elements 11-20)
- `example_chunk3.xml` (elements 21-30)
- `example_chunk4.xml` (elements 31-40)
- `example_chunk5.xml` (elements 41-50)

## Note

- The script assumes that the input XML files are well-formed and have a single root element.
- The chunked XML files will retain the structure of the original XML file, with each chunk having its root element.
- Existing files in the output folder with the same names as the generated chunks will be overwritten.

Feel free to adapt the script to suit your specific use case or requirements.
