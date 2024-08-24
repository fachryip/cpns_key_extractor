import os
import pathlib
import argparse
from pypdf import PdfReader 

input_path = './pdf/cpns_pemprov_2024.pdf'
formations = ['UMUM', 'TERBAIK', 'DISABILITAS']

def addinfo(line, row):
    # print(line)
    for formation in formations:
        if(formation in line):
            vs = line.split(formation)
            for v in vs:
                tmp = v.split(' ')
                if(len(tmp) > 3):
                    info = ""
                    if(tmp[0].isdigit()):
                        info = f"{formation} {tmp[0]} {tmp[1]} {tmp[2]} "
                    elif(tmp[1].isdigit()):
                        info = f"{formation} {tmp[1]} {tmp[2]} {tmp[3]} "
                    row = info + row
            break
    return row

def extract(input_path, output_path, keyword):
    valid_rows = []

    with open(input_path, 'rb') as f:
        reader = PdfReader(f)

        for page in reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            row = ""
            isfound = False

            for line in lines:
                if keyword in line:
                    isfound = True
                    
                    if 'ATASAN LANGSUNG' in row:
                        row = ""
                else:
                    front = line.split(' ')[0]
                    if(front.isdigit() and int(front) > 100):
                        if isfound:
                            valid_rows.append(row) 
                            isfound = False
                        row = ""
                row += line
                row = addinfo(line, row)

    output_folder = os.path.dirname(output_path)
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True) 

    with open(output_path, 'w') as f:
        for row in valid_rows:
            f.write(row + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='path after process')
    parser.add_argument('-k', help='key word to search for')
    args = parser.parse_args()
    # python main.py -o ./output/ilkom_pemprov_2024_2.txt -k 'ILMU KOMPUTER'
    extract(input_path, args.o, args.k)
    

