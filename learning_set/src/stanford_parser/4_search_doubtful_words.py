
import os
import re
import urllib2
import codecs
import string
import enchant

from xml.etree import ElementTree

def isint(value):
  try:
    int(value)
    return True
  except:
    return False



#You can change parameters to separate exactly what you need
def analysisDrugLines(input_file_path, dir_path):
    with codecs.open(input_file_path, "rt") as input_file:

        drugs_dict = {}
        for line in input_file:

            line = line.decode("windows-1252") #smth hack
            line = line.encode('ascii', 'ignore')
            rule = string.maketrans(u'!@#$%^&*()[]_=\\|<>,./?\'\":;', u'                          ')
            line = line.translate(rule).split()

            for word in line:
                #print word
                if isint(word):
                    continue
                #output_file.write(word + "\n")

                if drugs_dict.has_key(word):
                    drugs_dict[word] +=1
                else:
                    #print "get: " + word
                    drugs_dict.update({word: 1})

        #print drugs_dict.items()


        #Contain words with friquency above 1
        excluding_list = []
        eng_dict = enchant.Dict("en_US")

        for word, count in drugs_dict.items():
            #if count == 1:
            if not eng_dict.check(word):
                excluding_list.append(word)
            else:
                print word

        excluding_list.sort(key = len, reverse = True)
        #print excluding_dic

        #Output of doubtful words to manually check
        with codecs.open(dir_path + "doubtful_excess_words.txt", "wt", "utf-8") as output_file:
            output_file.write(' 0\n'.join(excluding_list))
            output_file.write('\n')

def searchDoubtfulDrugLines(input_file_path, output_file_path):
    with codecs.open(input_file_path, "rt", "utf-8") as input_file:
        with codecs.open(output_file_path, "wt", "utf-8") as output_file:
            doubtful_lines_count = 0
            for line in input_file:
                if len(line.split()) > 1:
                    output_file.write(line)
                    doubtful_lines_count += 1
            print str(doubtful_lines_count) + " lines are doubtful."


dir_path = './../../'
drug_names_file_path = './../../drug_names_without_NCT.txt'

doubtful_drug_sentences_file_path = './../../doubtful_drug_sentences.txt'






searchDoubtfulDrugLines(drug_names_file_path, doubtful_drug_sentences_file_path)
analysisDrugLines(doubtful_drug_sentences_file_path, dir_path)

