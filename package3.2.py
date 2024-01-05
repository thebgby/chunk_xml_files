
# imports
import xml.etree.ElementTree as ET      ## for parsing XML
import os       ## for file operations
import re ## for regular expressions

def extract_xml_declaration(xml_content):              ## function to extract the XML declaration
    match = re.match(r'^<\?xml .*?\?>', xml_content)   ## match the XML declaration
    if match:                                         ## if the match is not None
        return match.group()                        ## return the match
    else:                                              ## if the match is None
        return None                                  ## return None

def find_nearest_tag(root):               ## function to find the nearest tag
    for element in root.iter():           ## iterate through the root
        child_count = len(list(element))    ## get the number of children
        if child_count > 2:               ## if the number of children is greater than 2
            return list(element)[0].tag   ## return the tag of the first child

def get_outer_tags(tree):                                       ## function to get the outer tags 
    parent_map = {c.tag: p.tag for p in tree.iter() for c in p}     ## create a dictionary of parent tags and child tags
    child = find_nearest_tag(tree.getroot())                    ## get the nearest tag
    parents = []                                               ## create an empty list
    while parent_map.get(child, 0):                             ## while the child tag is in the parent_map
        parents.append(parent_map[child])                         ## append the parent tag to the parents list
        child = parent_map[child]                           ## set the child tag to the parent tag
    
    return parents[::-1]        ## return the parents list in reverse order

def create_element_tree(element_names, blocks):   ## function to create an element tree
    root = None                                   ## create a root element
    current_element = None                          ## create a current element

    for element_name in element_names:       ## iterate through the element names
        if root is None:                     ## if the root is None
            root = ET.Element(element_name)   ## create a root element 
            current_element = root              ## set the current element to the root
        else:
            new_element = ET.SubElement(current_element, element_name)    ## create a new element
            current_element = new_element                                   ## set the current element to the new element
         
    for block in blocks:                ## iterate through the blocks
        current_element.append(block)   ## append the block to the current element
 
    tree = ET.ElementTree(root)          ## create an element tree
    return tree                     ## return the element tree

def chunk_xml(xml_path, chunk_size, output_folder, header):   ## function to chunk the XML file
    tree = ET.parse(xml_path)                               ## parse the XML file
    root = tree.getroot()                                   ## get the root
    all_child_blocks = []                                   ## create an empty list
    for i in root.iter(find_nearest_tag(root)):             ## iterate through the root
        all_child_blocks.append(i)                             ## append the child to the all_child_blocks list
    file_name = os.path.basename(xml_path)                  ## get the file name
    for ind, i in enumerate(range(0, len(all_child_blocks), chunk_size)):       ## iterate through the all_child_blocks list
        default_tags = get_outer_tags(tree)                 ## get the outer tags
        tree_ = create_element_tree(default_tags, all_child_blocks[ind:ind+chunk_size])      ## create an element tree

        with open(f'{output_folder}/{ind+1}.xml', 'w') as f:    ## open a file
            if header is not None:                                  ## if the hea der is not None
                f.write(header)                                     ## write the header to the file
            f.write(ET.tostring(tree_.getroot(), method='xml').decode())    ## write the element tree to the file

def main(input_folder, chunk_size, output_folder):  ## main function
    if not os.path.exists(output_folder):                ## if the output folder does not exist
        os.makedirs(output_folder)                      ## create the output folder
    
    for file in os.listdir(input_folder):                   ## iterate through the files in the input folder
        if file.endswith('.xml'):                           ## if the file ends with .xml
            path = os.path.join(input_folder, file)         ## create the path
            with open(path, 'r') as f:                      ## open the file
                xml_content = f.readline()                  ## read the file
            header = extract_xml_declaration(xml_content)           ## extract the XML declaration
            chunk_xml(path, chunk_size, output_folder, header)  ## chunk the XML file

if __name__ == '__main__':
    main(r'inputfolder', 5, r'output_folder')
