# imports 
import os # for file handling
import xml.etree.ElementTree as ET # for XML parsing

def chunk_xml_files(input_folder, output_folder, chunk_size): # function to chunk XML files
    """
    Chunks XML files in input folder into chunks of size chunk_size and saves them in output folder.
    
    """

    os.makedirs(output_folder, exist_ok=True) # create output folder if it doesn't exist

    for filename in os.listdir(input_folder): # iterate through files in input folder
        if filename.endswith(".xml"): # if file is an XML file
            input_filepath = os.path.join(input_folder, filename) # get input file path

            tree = ET.parse(input_filepath) # parse XML file
            root = tree.getroot() # get root element

            total_elements = len(root) # get total number of elements in root element

            num_chunks = (total_elements + chunk_size - 1) // chunk_size # calculate number of chunks

            for i in range(num_chunks): # iterate through each chunk
                start_index = i * chunk_size # calculate start index
                end_index = min((i + 1) * chunk_size, total_elements) # calculate end index
                
                chunk_root = ET.Element(root.tag) # create chunk root element

                chunk_root.extend(root[start_index:end_index]) # add elements to chunk root element

                chunk_tree = ET.ElementTree(chunk_root) # create chunk tree

                output_filename = f"{filename.replace('.xml', f'_chunk{i + 1}.xml')}" # create output filename
                output_filepath = os.path.join(output_folder, output_filename) # create output filepath
                chunk_tree.write(output_filepath) # write chunk tree to output filepath

if __name__ == "__main__":
    input_folder = r"C:\Users\haske\OneDrive\Desktop\WORK\Package3\xmlfiles"
    output_folder = r"C:\Users\haske\OneDrive\Desktop\WORK\Package3\xmlfiles"
    chunk_size = 10

    chunk_xml_files(input_folder, output_folder, chunk_size)
