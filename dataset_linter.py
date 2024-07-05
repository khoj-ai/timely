from datetime import datetime
from tqdm import tqdm
import re 

# DESCRIPTION: converts existing dataset scheme into today: dates with YYYY-MM-DD format
dataset_to_convert = "datasets/wiki_mega_v5.txt"
output_file = "datasets/wiki_mega_v5_linted.txt"

def convert_date_format(date_str):
    # Convert MM/DD/YY to YYYY-MM-DD assuming dates are in the 2000s
    month, day, year = date_str.split("/")
    #clean year to only have digits
    year = ''.join(filter(str.isdigit, year))
    if int(year) < 100:
        year = "20" + year
    return year + "-" + month.zfill(2) + "-" + day.zfill(2)

def move_current_date_to_start(input_string):
    loc_date_start = input_string.find("current date:")
    input_string = input_string.replace("current date:", "currentxdate:", 1)
    if loc_date_start == -1:
        return input_string
    loc_date_end = loc_date_start
    while input_string[loc_date_end] != ' ' and input_string[loc_date_end] != '|' and loc_date_end < len(input_string)-1:
        #print(input_string[loc_date_start:loc_date_end])
        loc_date_end += 1
    date_str = input_string[loc_date_start:loc_date_end]
    date = date_str.split(":")[1].strip()
    new_date = convert_date_format(date)
    reformatted_string = input_string.replace(date_str, "")
    reformatted_string = "today:" + new_date + " " + reformatted_string
    return reformatted_string

# Read all lines at once with UTF-16 LE encoding and BOM handling
with open(dataset_to_convert,'rb') as f:
    contents = f.read()
    #print the type of contents
    print(type(contents))
contents = contents.decode("utf-16")
lines = contents.split("\n")

# Write to output file
with open(output_file, 'w', encoding="utf8", newline='') as file:
    for line in tqdm(lines, desc="Writing to output file", unit="line"):
        file.write(move_current_date_to_start(line).replace("  "," ") + "\n")
