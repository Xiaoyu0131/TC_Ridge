#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 18:33:26 2025

@author: xiaoyubai
"""

import pandas as pd
import numpy as np


colspecs = [(0, 80)]
file_path = '/Users/xiaoyubai/Documents/Data/Best_track/090425/bst_all.txt'

def parse_header(line):
    """Extract header information from the line."""
    # Extract fields based on fixed positions
    ID = line[6:11].strip().zfill(4)  # ID from position 6 to 11
    num_data_lines_str = line[12:15].strip()  # Number of data lines from position 12 to 15
    intense = line[16:20].strip()  # Intensity from position 16 to 20
    replicate = line[21:25].strip()  # Replicate from position 21 to 25
    flag = line[26:27].strip()  # Flag from position 26 to 27
    persistency = line[28:29].strip()  # Persistency from position 28 to 29
    cyclone_name = line[30:63].strip()  # Cyclone name from position 29 to 49
    update = line[64:79].strip().zfill(8)  # Update from position 64 to 71

    # Print extracted values for debugging
    # print(f"ID: '{ID}'")
    # print(f"Number of Data Lines: '{num_data_lines_str}'")
    # print(f"Intense: '{intense}'")
    # print(f"Replicate: '{replicate}'")
    # print(f"Flag: '{flag}'")
    # print(f"Persistency: '{persistency}'")
    # print(f"Cyclone Name: '{cyclone_name}'")
    # print(f"Update: '{update}'")

    # Convert num_data_lines to integer
    try:
        num_data_lines = int(num_data_lines_str)
    except ValueError:
        num_data_lines = 0  # Set default value if conversion fails

    # Return header dictionary
    header = {
        'ID': ID,
        'num_data_lines': num_data_lines,
        'intense': intense,
        'replicate': replicate,
        'flag': flag,
        'persistency': persistency,
        'cyclone_name': cyclone_name,
        'update': update
    }
    return header


def process_file(file_path):
    headers = []
    data_lines = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('66666'):
            # Parse header
            header = parse_header(line)
            headers.append(header)
            
            # Get number of data lines
            num_data_lines = header['num_data_lines']
            
            # Extract data lines
            data_lines_chunk = lines[i + 1:i + 1 + num_data_lines]
            for data_line in data_lines_chunk:
                data_line = data_line.strip()  # Ensure data line is stripped of any extra spaces
                if len(data_line) <= 28:
                    data_fields = {
                        'header_ID': header['ID'],
                        'header_intense': header['intense'],
                        'header_name' : header['cyclone_name'],
                        'data_time': data_line[0:8].strip().zfill(8),
                        'data_ID': data_line[9:12].strip().zfill(3),
                        'data_category': data_line[13:14].strip(),
                        'data_latitude': data_line[15:18].strip().zfill(3),
                        'data_longitude': data_line[19:23].strip().zfill(3),
                        'data_central_pressure': data_line[24:32].strip()                                                
                    }
                    data_lines.append(data_fields)
                elif len(data_line) <= 36:
                    # print(i)
                    data_fields = {
                        'header_ID': header['ID'],
                        'header_intense': header['intense'],
                        'header_name' : header['cyclone_name'],
                        'data_time': data_line[0:8].strip().zfill(8),
                        'data_ID': data_line[9:12].strip().zfill(3),
                        'data_category': data_line[13:14].strip(),
                        'data_latitude': data_line[15:18].strip().zfill(3),
                        'data_longitude': data_line[19:23].strip().zfill(3),
                        'data_central_pressure': data_line[24:32].strip(),
                        'data_max_sus_wind': data_line[33:40].strip()
                        }
                    data_lines.append(data_fields)
                else:
                    data_fields = {
                        'header_ID': header['ID'],
                        'header_intense': header['intense'],
                        'header_name' : header['cyclone_name'],
                        'data_time': data_line[0:8].strip().zfill(8),
                        'data_ID': data_line[9:12].strip().zfill(3),
                        'data_category': data_line[13:14].strip(),
                        'data_latitude': data_line[15:18].strip().zfill(3),
                        'data_longitude': data_line[19:23].strip().zfill(3),
                        'data_central_pressure': data_line[24:32].strip(),
                        'data_max_sus_wind': data_line[33:40].strip(),
                        'data_direction_50kt': data_line[41].strip(),
                        'data_long_radius_50kt': data_line[42:46].strip(),
                        'data_short_radius_50kt': data_line[47:51].strip(),
                        'data_direction_30kt': data_line[52].strip(),
                        'data_long_radius_30kt': data_line[53:57].strip(),
                        'data_short_radius_30kt': data_line[58:70].strip(),
                        'data_landfall': data_line[71:79].strip()
                        
                    }
                    data_lines.append(data_fields)
            
            # Move index to the next section
            i += 1 + num_data_lines
        else:
            # Skip non-header rows
            i += 1

    data_lines_df = pd.DataFrame(data_lines)

    return data_lines_df



# Process the file
data_lines_df = process_file(file_path)
data_lines_df.to_csv('/Users/xiaoyubai/Documents/TC_ridges_surface/data/adding_2324/TC_51-24_with_name.csv', index = None)
