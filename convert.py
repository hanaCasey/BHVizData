import json
import csv
import sys


#features of interest  and their marc21 code
columns = { 
'001': 'id',
'041' : 'language_code',
'049': 'holdings',
'100': 'author_person',
'110': 'author_corporate',
'111': 'author_meeting',
'111': 'author_uniform',
'245': 'title',
'264': 'publication',
'300': 'physical_description',
'600': 'subject_personal',
'610': 'subject_corporate',
'611': 'subject_meeting',
'630': 'subject_uniform_title',
'647': 'subject_named_event',
'648': 'subject_chronological',
'650': 'subject_topical',
'651': 'subject_geographic'}


input_files = sys.argv[1:-1]
output_path = 'data/'+ sys.argv[-1]

print(input_files, output_path)

#Write header once
with open(output_path, 'w', encoding='utf8') as out: 
    #Dictwriter for better performance
    writer = csv.DictWriter(out, fieldnames=columns.values())
    #Write header row: 
    writer.writeheader()

#gather all the info from the input files 
    for f in input_files:
        input_path = 'data/'+ f

        with open(input_path, encoding="utf8") as f_in: 
            data = json.load(f_in)

        rows = []

        for record in data['records'].values():
            rows += [{
                "id": record.get('001'),
                "041a": record.get('041', {}).get('a'), 
                "049": record.get('049'),
                "100a": record.get('100', {}).get('a'),
                "110a": record.get('110', {}).get('a'),
                "111a": record.get('111', {}).get('a'),
                "245a": record.get('245', {}).get('a'),
                "264a": record.get('264', {}).get('a'),
                "300a": record.get('300', {}).get('a'),
                "600a": record.get('600', {}).get('a'),
                "610a": record.get('610', {}).get('a'),
                "611a": record.get('611', {}).get('a'),
                "630a": record.get('630', {}).get('a'),
                "647a": record.get('647', {}).get('a'),
                "648a": record.get('648', {}).get('a'),
                "650a": record.get('650', {}).get('a'),
                "651a": record.get('651', {}).get('a')
                }]

        #write one file at once
        writer.writerows(rows)
        
        

