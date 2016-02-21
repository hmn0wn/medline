#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8") #hack to solve "import nltk unicodedecodeerror"

import os
import csv
import nltk.data

ntlk_path = './../../../../libs/nltk_data/tokenizers/punkt/english.pickle'
#ntlk_path = '/home/mikhail/nltk_data/tokenizers/punkt/english.pickle' #mikhail comp


def parseCsv(input_file_path, output_dir_path):
    csv_file = open(input_file_path, 'rt')

    tokenizer = nltk.data.load(ntlk_path)
    csvreader = csv.reader(csv_file)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    errors = 0;
    lines = 0;
    drug_lines = 0;
    for row in csvreader:
        lines += 1;
        print 'csv lile lint: ' + str(lines)
        index = row[0]
        text = row[1]
        cathegory = row[2]
        if cathegory != 'Drug':
            print 'not Drug'
            continue
        drug_lines += 1
        try:
            separated_text = ''
            for sentence in tokenizer.tokenize(text):
                separated_text += (sentence + '\n')

        except Exception:
            print " error in " + index
            errors += 1
            continue

        output_file = open(output_dir_path + '/' + str(index) + '.txt', 'wt')
        output_file.write(separated_text)
        output_file.close()
        print(index + ' successfully created')

    print str(errors) + ' errors of ' + str(lines) + ' samples.'
    print str(drug_lines) + ' Drug lines'
    output_file.close()
    csv_file.close()


csv_path = './../../NCTSLINK2015.csv'
separated_text_files_dir_path = './../../separated_drug_documents'
parseCsv(csv_path, separated_text_files_dir_path)

