import csv, os
import nltk.data
ntlk_path = '/home/amelub/pgm/libs/nltk_data/tokenizers/punkt/english.pickle'

def parseCsv(input, output):
    csv_file = open(input, 'rb')
    output_file = open(output, "w")
    tokenizer = nltk.data.load(ntlk_path)
    csvreader = csv.reader(csv_file)

    from stanford_parser.parser import Parser
    parser = Parser()

    errors = 0;
    lines = 0;
    for row in csvreader:
        lines += 1;
        print lines
        index = row[0]
        text = row[1]
        cathegory = row[2]

        try:
            output_file.writelines('+++++\n' + index + '\n+++++\n')
            for sentence in tokenizer.tokenize(text):
                #parser.parseToWordsWithTag(sentence, output_file)
                output_file.writelines(parser.parseToWordsWithTag(sentence))
            output_file.writelines('\n-----\n' + cathegory + '\n-----\n')

        except Exception:
            print " error in " + index
            output_file.writelines('\n-----\n' + cathegory + '\n-----\n')
            errors += 1

    print str(errors) + ' errors of ' + str(lines) + ' samples.'
    output_file.close()
    csv_file.close()


#-----------------------------------------------------------------------------

def parseTextFile(input, output):
    text_file = open(input, 'rb')
    output_text_file = open(output, "w")
    tokenizer = nltk.data.load(ntlk_path)

    from stanford_parser.parser import Parser
    parser = Parser()

    text = text_file.read()

    try:
        for sentence in tokenizer.tokenize(text):
            #parser.parseToWordsWithTag(sentence, output_file)
            output_text_file.writelines(parser.parseToWordsWithTag(sentence))
            output_text_file.writelines('\n-----\n')

    except Exception:
        print " error "


    output_text_file.close()
    text_file.close()


csv_path = './../../NCTSLINK2015.csv'
output_path ="./../../output.txt"
parseCsv(csv_path, output_path)

text_path = '/home/amelub/Documents/letitaciya'
output_text_path ="/home/amelub/Documents/letitaciya_NLP"
#parseTextFile(text_path, output_text_path)



