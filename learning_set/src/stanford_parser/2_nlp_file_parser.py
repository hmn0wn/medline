import os
import nltk.data
import codecs
#ntlk_path = '/home/amelub/pgm/libs/nltk_data/tokenizers/punkt/english.pickle'

def parseDirOfTextFiles(input_dir_path, output_dir_path):

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    from stanford_parser.parser import Parser
    parser = Parser()

    errors = 0
    files = 0
    list_of_files = os.listdir(input_dir_path)
    for filename in list_of_files:

        tagget_words = ''
        files += 1
        print str(files) + '/1620 file:'
        try:
            with codecs.open(input_dir_path + '/' + str(filename), 'rt', 'utf-8') as input_text_file:
                for sentence in input_text_file:
                    #print sentence
                    tagget_words += parser.parseToWordsWithTag(sentence[:-1]) + "\n"
                    #print tagget_words

        except Exception:
            errors  += 1
            print str(errors)+ " error in " + filename
            continue

        output_file = codecs.open(output_dir_path + '/' + filename, 'wt', 'utf-8')
        output_file.write(tagget_words)
        output_file.close()
        print( filename  + ' successfully created')


    print str(errors) + ' errors of ' + str(files) + ' files.'

    #     lines += 1;
    #     print lines
    #     index = row[0]
    #     text = row[1]
    #     cathegory = row[2]
    #
    #     try:
    #         output_file.writelines('+++++\n' + index + '\n+++++\n')
    #         for sentence in tokenizer.tokenize(text):
    #             #parser.parseToWordsWithTag(sentence, output_file)
    #             output_file.writelines(parser.parseToWordsWithTag(sentence))
    #         output_file.writelines('\n-----\n' + cathegory + '\n-----\n')
    #
    #     except Exception:
    #         print " error in " + index
    #         output_file.writelines('\n-----\n' + cathegory + '\n-----\n')
    #         errors += 1
    #
    # print str(errors) + ' errors of ' + str(lines) + ' samples.'
    # output_file.close()
    # csv_file.close()


#-----------------------------------------------------------------------------

# def parseTextFile(input, output):
#     text_file = open(input, 'rb')
#     output_text_file = open(output, "w")
#     tokenizer = nltk.data.load(ntlk_path)
#
#     from stanford_parser.parser import Parser
#     parser = Parser()
#
#     text = text_file.read()
#
#     try:
#         for sentence in tokenizer.tokenize(text):
#             #parser.parseToWordsWithTag(sentence, output_file)
#             output_text_file.writelines(parser.parseToWordsWithTag(sentence))
#             output_text_file.writelines('\n-----\n')
#
#     except Exception:
#         print " error "
#
#
#     output_text_file.close()
#     text_file.close()


csv_path = './../../NCTSLINK2015.csv'
separated_text_files_dir_path = './../../separated_drug_documents'
tagged_text_files_path = './../../separated_drug_documents_with_tags'
parseDirOfTextFiles(separated_text_files_dir_path, tagged_text_files_path)

#text_path = '/home/amelub/Documents/letitaciya'
#output_text_path ="/home/amelub/Documents/letitaciya_NLP"
#parseTextFile(text_path, output_text_path)



