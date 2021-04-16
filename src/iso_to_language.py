import csv

iso_to_lang = dict()

with open('../data/iso-639-3.tab') as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        iso_to_lang[row['Id']] = row['Ref_Name']

print(iso_to_lang["eng"])