"""
Script Name: SCVR.py
Version: 2.0.2
Author: Kory Kinnett
Date: December 2023

Description:
This script modifies your attributes.xml's FOV, Height, Width, WindowMode, VSync attributes. It allows a user to select preset settings for specific (30) headsets and their respective (80) lens/fov configurations.'
"""

import json
import xml.etree.ElementTree as ET
import re

def load_configurations(filename):
    with open(filename, 'r') as file:
        configurations = json.load(file)
    return configurations

def update_xml_config(xml_filename, fov, height, width):
    tree = ET.parse(xml_filename)
    root = tree.getroot()

    for attr in root.findall(".//Attr"):
        if attr.attrib["name"] == "FOV":
            attr.set("value", str(fov))
        elif attr.attrib["name"] == "Height":
            attr.set("value", str(height))
        elif attr.attrib["name"] == "Width":
            attr.set("value", str(width))

    # Find the position to insert VSync and WindowMode attributes
    last_attr_position = root.findall(".//Attr")[-1]

    # Use insert method to add elements at specific positions
    root.insert(root.getchildren().index(last_attr_position) + 1, ET.Element("Attr", {"name": "VSync", "value": "0"}))
    root.insert(root.getchildren().index(last_attr_position) + 2, ET.Element("Attr", {"name": "WindowMode", "value": "2"}))

    tree.write(xml_filename)

def print_ordered_options(options):
    for index, option in enumerate(options, 1):
        print(f"{index}) {option}")

def show_additional_resolutions(resolutions):
    print("\nOptions:")
    for index, resolution in enumerate(resolutions):
        print(f"{index + 1}. {resolution}")

    option_index = int(input("\nEnter the option index: ")) - 1
    return resolutions[option_index]

def main():
    json_filename = 'SCVR.json'
    xml_filename = 'attributes.xml'

    configurations = load_configurations(json_filename)

    # Prompt user for brand selection
    available_brands = sorted(set(configurations[key]["Headset Brand"] for key in configurations))
    print("Available headset brands:")
    for index, brand in enumerate(available_brands, 1):
        print(f"{index}. {brand}")
    
    brand_index = int(input("Enter the index of the desired headset brand: ")) - 1
    selected_brand = available_brands[brand_index]

    # Prompt user for headset model selection
    available_models = sorted(set(f"{configurations[key]['Headset Brand']} {configurations[key]['Headset Model']}" for key in configurations if configurations[key]["Headset Brand"] == selected_brand))
    print(f"Available headset models for {selected_brand}:")
    for index, model in enumerate(available_models, 1):
        print(f"{index}. {model}")
    
    model_index = int(input("Enter the index of the desired headset model: ")) - 1
    selected_model_full = available_models[model_index]
    
    # Extracting only the model name from the full string
    selected_model = selected_model_full.split(maxsplit=1)[-1]

    # Find the correct key for the selected brand and model
    for key in configurations:
        if configurations[key]["Headset Brand"] == selected_brand and configurations[key]["Headset Model"] == selected_model:
            break
    else:
        print("Selected brand and model not found in the configurations.")
        return

    # Check if there's only one lens configuration available
    available_lens_configs = configurations[key]["All Possible Lens Configurations"]
    available_lens_configs = [config for config in available_lens_configs if config != "Choose One"]

    if len(available_lens_configs) == 1:
        selected_lens_config = available_lens_configs[0]
    else:
        # Prompt user for lens configuration selection
        print(f"Available lens configurations for {selected_brand} {selected_model}:")
        for index, lens_config in enumerate(available_lens_configs, 1):
            print(f"{index}. {lens_config}")
        lens_index = int(input("Enter the index of the desired lens configuration: ")) - 1
        selected_lens_config = available_lens_configs[lens_index]

    # Prompt user for resolution selection
    available_resolutions = configurations[key]["Custom Resolution List"]
    
    # Sort resolutions based on the ending % value
    available_resolutions.sort(key=lambda x: float(re.search(r'(\d+)%', x).group(1)) if re.search(r'(\d+)%', x) else float('inf'))

    # Print list of resolutions
    for index, resolution in enumerate(available_resolutions, 1):
        print(f"{index}. {resolution}")
    
    # Lastly, print alt resolution option.
    additional_resolutions_option = "Show Additional Resolutions"
    additional_option_index = len(available_resolutions) + 1
    print(f"{additional_option_index}. {additional_resolutions_option}")
    option_index = int(input("\nEnter the option index: "))
    
    # Initialize height and width variables
    height = width = 0

    # Check if the user selected the alternative resolution option
    if option_index == additional_option_index:
        # Additional resolutions
        resolution_type_options = [
            "Alternative Interger Resolutions (small list)",
            "Alternative Interger Resolutions (big list)",
            "Give me all the resolutions"
        ]
        selected_resolution_type = show_additional_resolutions(resolution_type_options)
        
        # Use the selected resolution type to filter the resolutions
        additional_resolutions = configurations[key].get(selected_resolution_type, [])
        if additional_resolutions:
            additional_option_index += len(resolution_type_options)
            print_ordered_options(additional_resolutions)
            additional_resolution_index = int(input("\nEnter the resolution index: ")) - 1
            selected_resolution = additional_resolutions[additional_resolution_index]
            
            # Extract numeric values from the resolution string
            match = re.search(r'(\d+)\s*X\s*(\d+)', selected_resolution)
            if match:
                width, height = map(int, match.groups())
    else:
        # User selected a resolution from the available list
        selected_resolution = available_resolutions[option_index - 1]

        # Extract numeric values from the resolution string
        match = re.search(r'(\d+)\s*X\s*(\d+)', selected_resolution)
        if match:
            width, height = map(int, match.groups())
        else:
            print("Invalid resolution format. Please enter resolutions in the format 'width X height'.")

    # Update XML file with selected values
    update_xml_config(xml_filename, configurations[key]["SC Attributes FOV"], height, width)
   
    # Get the recommended VorpX Config Pixel 1:1 Zoom value
    vorpx_config_zoom = configurations[key]["VorpX Config Pixel 1:1 Zoom"]

    # Print all selections made by the user
    print("\nSelected Configuration:")
    print(f"Headset: {selected_brand} {selected_model}")
    print(f"Lens Configuration: {selected_lens_config}")
    print(f"Resolution: {selected_resolution}")
    # Print fixed values
    print("SC window mode set to Borderless")
    print("VSync has been disabled (recommended)")
    # Print pre-calculated zoom-variable
    print(f"\033[1mRecommended setting your VorpX Pixel 1:1 Zoom value to at least {vorpx_config_zoom} if able.\033[0m")
    # Inform User of Completion of Code
    print("\nConfiguration updated successfully!")

    # Additional print line for alternative resolutions
    if option_index == additional_option_index:
        print(f"\nSelected Alternative Resolution: {selected_resolution}")

if __name__ == "__main__":
    main()

    # Pause to allow the user to see and take note of the vorpx zoom value
    input("Press Enter to close... Else, you can close me now.")