from datetime import datetime
from tqdm import tqdm
import re 

# DESCRIPTION: converts existing dataset scheme into today: dates with YYYY-MM-DD format
dataset_to_convert = "datasets/gooaq_v2.csv"
output_file = "datasets/gooaq_v3.txt"

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
    #if current date is not found search for today: instead
    if loc_date_start == -1:
        loc_date_start = input_string.find("today:")
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
contents = contents.decode("utf8")
lines = contents.split("\n")

# Write to output file
with open(output_file, 'w', encoding="utf8", newline='') as file:
    for line in tqdm(lines, desc="Writing to output file", unit="line"):
        try:
            reformatted_string = move_current_date_to_start(line)
            #remove newlines and double space from reformatted_string
            reformatted_string = reformatted_string.replace("  ", " ")
            reformatted_string = reformatted_string.replace("\n", "")
            query = reformatted_string.split("|")[0]
            doc = reformatted_string.split("|")[1]
            #if there are two | extract the [2] entry which is the score
            if len(reformatted_string.split("|")) > 2:
                doc2 = reformatted_string.split("|")[2]
                score = reformatted_string.split("|")[3]
                file.write(query+"|"+doc+"|"+doc2+"|"+score)
            else:
                file.write(query+"|"+doc)
        except:
            continue
            # print("Error in line: ", line)