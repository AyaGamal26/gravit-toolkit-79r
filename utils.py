import os
import xml.etree.ElementTree as ET
import copy

def load_svg(file_path):
    """Load an SVG file and return its ElementTree."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"SVG file not found: {file_path}")
    
    try:
        tree = ET.parse(file_path)
        return tree
    except ET.ParseError as e:
        raise ValueError(f"Error parsing SVG file: {file_path}. Error: {e}")

def save_svg(tree, output_path):
    """Save the ElementTree to an SVG file."""
    try:
        tree.write(output_path, xml_declaration=True, encoding='utf-8')
        print(f"Successfully saved SVG to: {output_path}")
    except Exception as e:
        raise IOError(f"Failed to save SVG file: {output_path}. Error: {e}")

def extract_layers(svg_tree):
    """Extract layers from the SVG tree and return a list of layers."""
    root = svg_tree.getroot()
    layers = []
    
    # This assumes that layers are grouped under <g> tags with a specific class
    for g in root.findall('.//{http://www.w3.org/2000/svg}g'):
        layer_id = g.get('id')
        if layer_id and 'layer' in layer_id.lower():  # Assuming layers have 'layer' in the id
            layers.append(g)
    
    if not layers:
        raise ValueError("No layers found in the SVG file.")
    
    return layers

def create_layer_svg(layer, output_dir, layer_name, original_root):
    """Create a new SVG file for the given layer."""
    # Create new SVG root element with proper attributes
    svg_root = ET.Element('svg')
    svg_root.set('xmlns', 'http://www.w3.org/2000/svg')
    
    # Copy attributes from original SVG if they exist
    for attr in ['width', 'height', 'viewBox']:
        if original_root.get(attr):
            svg_root.set(attr, original_root.get(attr))
    
    # Create a deep copy of the layer to avoid modifying the original
    layer_copy = copy.deepcopy(layer)
    svg_root.append(layer_copy)
    
    layer_tree = ET.ElementTree(svg_root)
    output_path = os.path.join(output_dir, f"{layer_name}.svg")
    
    save_svg(layer_tree, output_path)

def export_layers_from_svg(input_svg, output_dir):
    """Export all layers from the input SVG file into separate SVG files."""
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    svg_tree = load_svg(input_svg)
    layers = extract_layers(svg_tree)
    original_root = svg_tree.getroot()

    for layer in layers:
        layer_name = layer.get('id') or 'layer'  # Default name if id is not present
        create_layer_svg(layer, output_dir, layer_name, original_root)

# TODO: Add functionality to handle different SVG namespaces
# TODO: Implement logging instead of print statements for better debugging
# TODO: Consider adding support for user-defined layer filters (e.g., by name)
