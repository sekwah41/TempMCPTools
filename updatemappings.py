import requests
import csv
from os.path import expanduser, join, basename, exists
import re

legal_name = re.compile('([a-zA-Z_0-9])*')
bad_start = re.compile('([0-9])')

def downloadMappings():
    print("Downloading mappings")
    response = requests.get(
        'https://docs.google.com/spreadsheet/ccc?key=14knNUYjYkKkGpW9VTyjtlhaCTUsPWRJ91GLOFX2d23Q&output=csv',
        stream=True)
    fullDumpFile = "fulldump.csv"
    assert response.status_code == 200, 'Could not download file'

    with open(fullDumpFile, 'wb') as f:
        block_size = 1024
        total_length = int(response.headers.get('content-length', 0))
        for data in response.iter_content(block_size):
            f.write(data)

    print("Done")


def convertToMCP():
    with open('fulldump.csv') as csv_file:
        fields = open('projectmappings/fields.csv', 'w')
        methods = open('projectmappings/methods.csv', 'w')
        params = open('projectmappings/params.csv', 'w')
        raw_mappings = csv.reader(csv_file, delimiter=',')
        line_number = 0
        for row in raw_mappings:
            if line_number == 0:
                print(f'Column names are {", ".join(row)}')
            elif len(row) != 6:
                print(f"Warning at entry, incorrect number of entries {row}")
            elif row[0] == "TRUE" and row[2] != "" and row[3] != "" and row[4] != "":
                if row[2].find(" ") != -1 or row[3].find(" ") != -1:
                    print(f"Warning at entry {row}")
                elif bad_start.match(row[3]) or not legal_name.match(row[3]).span()[1] == len(row[3]):
                    print(f"Bad name detected {row}")
                else:
                    line = f"{row[2]},{row[3]},{row[4]},{row[5]}\n"
                    if row[2].startswith("field_"):
                        fields.write(line)
                    elif row[2].startswith("func_"):
                        methods.write(line)
                    elif row[2].startswith("p_"):
                        params.write(line)
            line_number += 1
        fields.close()
        methods.close()
        params.close()
    print("Converted")


# searge,name,side,desc
def sortAndMerge(file):
    original = open(f'original/{file}')
    additional = open(f'projectmappings/{file}')
    target = open(f'merged/{file}', 'w')

    fields = {}

    original_csv = csv.reader(original, delimiter=',')
    additional_csv = csv.reader(additional, delimiter=',')

    line_number = 0
    for line in original_csv:
        # Don't need to filter first line as none are ever called searge ;)
        if line[0] not in fields:
            target.write(",".join(line) + "\n")
        fields[line[0]] = line[1]
        line_number += 1

    for line in additional_csv:
        # Don't need to filter first line as none are ever called searge ;)
        if line[0] not in fields:
            target.write(",".join(line) + "\n")
        fields[line[0]] = line[1]
        line_number += 1

    print(f"Written lines {line_number} to {file}")

    original.close()
    additional.close()
    target.close()


fileNames = ["fields.csv", "methods.csv", "params.csv"]

if (len([a for a in fileNames if exists(f"original/{a}")])) != 3:
    exit("Original mappings to merge not detected")

downloadMappings()
convertToMCP()

for file in fileNames:
    sortAndMerge(file)
print("Finished Merging")
