import xml.etree.ElementTree as ET
import os, re

def extract_xml_declaration(xml_content):
    match = re.match(r'^<\?xml .*?\?>', xml_content)
    if match:
        return match.group()
    else:
        return None

with open('meditech.xml', 'r') as file:
    xml_content = file.readline()
def find_nearest_tag(root):
   
   for element in root.iter():
      child_count = len(list(element))
      if child_count > 2:
         return list(element)[0].tag

def chunk_xml(xml_path, chunk_size, output_folder, header):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    all_child_blocks=[]
    for i in root.iter(find_nearest_tag(root)):
        a=ET.tostring(i)
        all_child_blocks.append(a)


    for ind, i in enumerate(range(0,len(all_child_blocks),chunk_size)):
        root = ET.Element(root.tag)
        for childs in all_child_blocks[i:i+chunk_size]:    
            root.append(ET.fromstring(childs))

        tree_ = ET.ElementTree(root)
        tree_ = ET.tostring(tree_.getroot(), encoding='utf-8').decode('utf-8')
        
        with open(f'{output_folder}/{ind+1}.xml','w') as f:
            if header is not None:
                f.write(header)
            f.write(str(tree_))

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


main(r'C:\Users\haske\OneDrive\Desktop\WORK\Package3\meditech.xml',100,r'C:\Users\haske\OneDrive\Desktop\WORK\Package3')