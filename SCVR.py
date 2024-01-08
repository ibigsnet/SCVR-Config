"""
Script Name: SCVR.py
Version: 3.0.0
Author: Kory Kinnett
Date: January 2024

Description:
This script can modify your attributes.xml's FOV, Height, Width, WindowMode, VSync, MotionBlur, OverscanBorder, GForceZoomScale, AutoZoomOnSelectedTargetStrength, ShakeScale, Sharpening, ChromaticAberration, FilmGrain, ScatterDist and TerrainTessDistance attributes. It allows a user to select preset settings for specific (31) headsets and their respective (83) lens/fov configurations.'
"""

import json
import xml.etree.ElementTree as ET
import re

def load_configurations(filename):
    with open(filename, 'r') as file:
        configurations = json.load(file)
    return configurations

#def update_xml_config(xml_filename, fov, height, width, scatterdistance, tesselation):
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
        elif attr.attrib["name"] == "VSync":
            attr.set("value", "0")
        elif attr.attrib["name"] == "WindowMode":
            attr.set("value", "2")
        elif attr.attrib["name"] == "MotionBlur":
            attr.set("value", "0")
        elif attr.attrib["name"] == "GForceZoomScale":
            attr.set("value", "0")
        elif attr.attrib["name"] == "GForceHeadBobScale":
            attr.set("value", "1")
        elif attr.attrib["name"] == "AutoZoomOnSelectedTargetStrength":
            attr.set("value", "1")
        elif attr.attrib["name"] == "ShakeScale":
            attr.set("value", "1")
        elif attr.attrib["name"] == "Sharpening":
            attr.set("value", "1")
        elif attr.attrib["name"] == "ChromaticAberration":
            attr.set("value", "0")
        elif attr.attrib["name"] == "FilmGrain":
            attr.set("value", "0")
        #elif attr.attrib["name"] == "ScatterDist":
        #    attr.set("value", str(scatter))
        #elif attr.attrib["name"] == "TerrainTessDistance":
        #    attr.set("value", str(tesselation))

    tree.write(xml_filename)

def print_ordered_options(options):
    for index, option in enumerate(options, 1):
        print(f"{index}) {option}")

def show_additional_resolutions(resolutions):
    print("\nOptions:")
    for index, resolution in enumerate(resolutions, 1):
        print(f"{index}. {resolution}")

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
    
    # Initialize selected_resolution variable
    selected_resolution = ""
    
    # Check if the user selected the alternative resolution option
    if option_index == additional_option_index:
        # Additional resolutions
        resolution_type_options = [
            "Alternative Integer Resolutions (small list)",
            "Alternative Integer Resolutions (big list)",
            "Give me all the resolutions"
        ]
        selected_resolution_type = show_additional_resolutions(resolution_type_options)
    
        # Use the selected resolution type to filter the resolutions
        additional_resolutions = configurations[key].get(selected_resolution_type, [])
        if additional_resolutions:
            # Print additional resolution options
            print_ordered_options(additional_resolutions)
    
            # Prompt user for additional resolution selection
            additional_resolution_index = int(input("\nEnter the resolution index: ")) - 1
            selected_resolution = additional_resolutions[additional_resolution_index]
    
            # Extract numeric values from the resolution string
            match = re.search(r'(\d+)\s*X\s*(\d+)', selected_resolution, re.IGNORECASE)
            if match:
                width, height = map(int, match.groups())
    else:
        # User selected a resolution from the available list
        if 0 < option_index <= len(available_resolutions):
            selected_resolution = available_resolutions[option_index - 1]
    
            # Extract numeric values from the resolution string
            match = re.search(r'(\d+)\s*X\s*(\d+)', selected_resolution)
            if match:
                width, height = map(int, match.groups())
            # Not really needed... but we'll check for errors anyways
            else:
                print("Invalid resolution format. Please enter resolutions in the format 'width X height'.")
        else:
            print("Invalid option index selected for resolution.")
            
    # Debug Print values for debugging
    #print(f"FOV: {configurations[key]['SC Attributes FOV']}")
    #print(f"Height: {height}, Width: {width}")
    
    # Update XML file with selected values
    update_xml_config(xml_filename, configurations[key]["SC Attributes FOV"], height, width)
    
    # Debug Print values after updating XML file for debugging
    #print("Values after updating XML:")
    #print(f"FOV: {configurations[key]['SC Attributes FOV']}")
    #print(f"Height: {height}, Width: {width}")
    
    # Get the recommended VorpX Config Pixel 1:1 Zoom value
    vorpx_config_zoom = configurations[key]["VorpX Config Pixel 1:1 Zoom"]

    # Print all selections made by the user
    print("\nSelected Configuration:")
    print(f"Headset: {selected_brand} {selected_model}")
    print(f"Lens Configuration: {selected_lens_config}")
        # Resolution print lines
    if option_index == additional_option_index:
        print(f"\nSelected Alternative Resolution: {selected_resolution}")
    else:
        print(f"Resolution: {selected_resolution}")
    # Print fixed values
    print("SC window mode set to Borderless")
    print("VSync has been disabled (recommended)")
    print(f"Game FOV set to {configurations[key]['SC Attributes FOV']}")
    # Print pre-calculated zoom-variable
    print(f"\033[1mRecommended setting your VorpX Pixel 1:1 Zoom value to at least {vorpx_config_zoom} if able.\033[0m")
    # Inform User of Completion of Code
    print("\nConfiguration updated successfully!")

if __name__ == "__main__":
    main()

    # Pause to allow the user to see and take note of the vorpx zoom value
    input("Press Enter to close... Else, you can close me now.")
