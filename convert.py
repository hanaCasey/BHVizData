import tarfile
import os
import json
import csv

COLUMNS = ['id', 'lang', 'authors', 'title', 'subtitle', 'statement', 'place', 
           'publisher', 'year', 'editors', 'subjects', 
           'subject_types', 'parentId', 'parentTitle']

input_file = 'data/b3kat_export_202211_enhanced.gz'


# create output folder

out_folder_path = 'data/csv_files'

try: 
    os.mkdir(out_folder_path)
except FileExistsError: 
    print(f"Directory {out_folder_path} already exists.")
    

with tarfile.open(input_file, "r:gz") as tar:

    for member in tar.getmembers():

        #extract the file contents as string

        file = tar.extractfile(member)

        #create output path for output file

        output_path = os.path.join(out_folder_path , member.name.replace('.json','.csv'))

        with open(output_path, 'w', encoding='utf8') as out: 

            #Dictwriter for better performance, write header

            writer = csv.DictWriter(out, fieldnames=COLUMNS)
            writer.writeheader()

            # read json data 

            json_data = file.read().decode('utf8')

            #convert into json

            data = json.loads(json_data)

            rows = []

            for record in data['records']:

                #possible arrays of values
                
                authors = '|'.join([a['name'] for a in record.get('authors',[])])
                editors = '|'.join([e['name'] for e in record.get('editors',[])])
                subjects = '|'.join([s['word'] for s in record.get('keywords',[])])
                subject_types = '|'.join([s['type'] for s in record.get('keywords',[])])

                # construct row for one entry

                rows += [{
                    'id': record.get('id'), 
                    'lang': record.get('lang', [None])[0], 
                    'authors': authors, 
                    'title': record.get('title'), 
                    'subtitle': record.get('subtitle'),
                    'statement': record.get('statement'), 
                    'place': record.get('place'), 
                    'publisher': record.get('publisher'), 
                    'year': record.get('year'), 
                    'editors': editors, 
                    'subjects': subjects,
                    'subject_types': subject_types, 
                    'parentId': record.get('parentId'), 
                    'parentTitle': record.get('parentTitle'), 
                    }]


            # write rows for one file at once  
            writer.writerows(rows)



# #testing with one file

# path = 'data/b3kat_export_202211_teil01.json'
# output_path= 'data/out_test.csv'

# #Open output file only once

# with open(output_path, 'w', encoding='utf8') as out: 

#     #Dictwriter for better performance, write header

#     writer = csv.DictWriter(out, fieldnames=COLUMNS)
#     writer.writeheader()


#     # open file and read json 

#     with open(path, encoding="utf8") as f: 

#         data = json.load(f)
#         rows = []


#         #tbc
        
#         for record in data['records']:

#             #possible arrays of values
#             authors = '|'.join([a['name'] for a in record.get('authors',[])])
#             editors = '|'.join([e['name'] for e in record.get('editors',[])])
#             subjects = '|'.join([s['word'] for s in record.get('keywords',[])])
#             subject_types = '|'.join([s['type'] for s in record.get('keywords',[])])

#             # construct row for one entry

#             rows += [{
#                 'id': record.get('id'), 
#                 'lang': record.get('lang', [None])[0], 
#                 'authors': authors, 
#                 'title': record.get('title'), 
#                 'subtitle': record.get('subtitle'),
#                 'statement': record.get('statement'), 
#                 'place': record.get('place'), 
#                 'publisher': record.get('publisher'), 
#                 'year': record.get('year'), 
#                 'editors': editors, 
#                 'subjects': subjects,
#                 'subject_types': subject_types, 
#                 'parentId': record.get('parentId'), 
#                 'parentTitle': record.get('parentTitle'), 
#                 }]


#     # write rows for one file at once  
#     writer.writerows(rows)



