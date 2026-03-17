import os
import xml.etree.ElementTree as ET
import copy
import re

def export_layers_from_svg(svg_file, output_dir):
    """
    Exports each layer from the given SVG file into separate SVG files.

    :param svg_file: Path to the input SVG file.
    :param output_dir: Directory where the exported layers will be saved.
    """
    if not os.path.isfile(svg_file):
        raise FileNotFoundError(f"The file {svg_file} does not exist.")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()
        
        # SVG namespace handling
        namespaces = {
            'svg': 'http://www.w3.org/2000/svg',
            'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
        }
        
        # Find all layer groups in the SVG
        layers = root.findall('.//svg:g[@inkscape:label]', namespaces=namespaces)
        
        if not layers:
            print("No layers found in the SVG file.")
            return
        
        for i, layer in enumerate(layers):
            layer_id = layer.get('id')
            layer_name = layer.get('{http://www.inkscape.org/namespaces/inkscape}label')
            
            # Handle missing or invalid layer names
            if not layer_name:
                layer_name = layer_id if layer_id else f"layer_{i+1}"
            
            # Sanitize layer name for filename
            safe_layer_name = re.sub(r'[<>:"/\\|?*]', '_', layer_name)
            
            # Create a new SVG root for the exported layer
            new_root = ET.Element('svg')
            new_root.set('xmlns', 'http://www.w3.org/2000/svg')
            new_root.set('width', root.get('width'))
            new_root.set('height', root.get('height'))
            
            # Copy the layer to the new SVG root
            layer_copy = copy.deepcopy(layer)
            new_root.append(layer_copy)
            
            # Generate output file path
            layer_file_name = f"{safe_layer_name}.svg"
            layer_file_path = os.path.join(output_dir, layer_file_name)
            
            # Write the new SVG file
            new_tree = ET.ElementTree(new_root)
            new_tree.write(layer_file_path, encoding='utf-8', xml_declaration=True)
            print(f"Exported layer '{layer_name}' to '{layer_file_path}'")
    
    except ET.ParseError as e:
        print(f"Error parsing SVG file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # TODO: Add command line interface for better user interaction
    svg_file_path = input("Enter the path to the SVG file: ")
    output_directory = input("Enter the output directory for exported layers: ")
    
    export_layers_from_svg(svg_file_path, output_directory)
