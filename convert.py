import tarfile
import sys
import json
import csv

COLUMNS = ['id', 'lang', 'authors', 'title', 'statement', 'place', 'publisher', 'year', 'contents', 'illustrations', 'keywords', 'parentId', 'parentTitle']

input_file = sys.argv[1]

#for later use 
# with tarfile.open(input_file, "r:gz") as tar:

#     for index, item in enumerate(tar):

#         #ectract the file contents as string
#         file = tar.extractfile(item)
#         json_data = file.read().decode('utf8')

#         #convert into json
#         data = json.loads(json_data)



#testing with one file

path = 'data/b3kat_export_202211_teil01.json'
output_path= 'data/out_test.csv'

#Write header once
with open(output_path, 'w', encoding='utf8') as out: 

    #Dictwriter for better performance
    writer = csv.DictWriter(out, fieldnames=COLUMNS)
    writer.writeheader()


    with open(path, encoding="utf8") as f: 

         data = json.load(f)

    rows = []


    #tbc
    for record in data['records'].values():
        rows += [{
            'id': record.get('id'), 
            'lang': record.get('lang')[0]
            }]




