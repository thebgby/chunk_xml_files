import xml.etree.ElementTree as ET
import os, re

def extract_xml_declaration(xml_content):
    match = re.match(r'^<\?xml .*?\?>', xml_content)
    if match:
        return match.group()
    else:
        return None


def find_nearest_tag(root):
   
   for element in root.iter():
      child_count = len(list(element))
      if child_count > 2:
         return list(element)[0].tag

def get_outer_tags(tree):
    parent_map = {c.tag: p.tag for p in tree.iter() for c in p}
    child = find_nearest_tag(tree.getroot())
    parents=[]
    while parent_map.get(child,0):
        parents.append(parent_map[child])
        child = parent_map[child]
    
    return parents[::-1]

def create_element_tree(element_names, blocks):
    root = None
    current_element = None

    for element_name in element_names:
        if root is None:
            # If root is not yet created, create it
            root = ET.Element(element_name)
            current_element = root
        else:
            # If root is already created, create child elements
            new_element = ET.SubElement(current_element, element_name)
            current_element = new_element
        
    for block in blocks:
        current_element.append(block)
        
        
    tree = ET.ElementTree(root)
    return tree

def chunk_xml(xml_path, chunk_size, output_folder, header):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    all_child_blocks=[]
    for i in root.iter(find_nearest_tag(root)):
        all_child_blocks.append(i)


    for ind, i in enumerate(range(0,len(all_child_blocks),chunk_size)):
        default_tags = get_outer_tags(tree)
        tree_ = create_element_tree(default_tags,all_child_blocks[ind:ind+chunk_size])

        with open(f'{output_folder}/{ind+1}.xml','w') as f:
            # if header is not None:
            #     f.write(header)
            tree_.write(f'{output_folder}/{ind+1}.xml',xml_declaration=True)

def main(input_folder, chunk_size, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs('output')
    for file in os.listdir(input_folder):
        if file.endswith('.xml'):
            path = os.path.join(input_folder,file)
            with open(path,'r') as f:
                xml_content = f.readline()
            header = extract_xml_declaration(xml_content)
            chunk_xml(path, chunk_size, output_folder, header)


main('xmlfile',5,'output')