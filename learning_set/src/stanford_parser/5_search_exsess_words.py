
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


def convert0To1(input_file_path):
    with codecs.open(input_file_path, 'rt') as input_file:
        output_text = ''
        for line in input_file:
            list_line = line.split()
            #print  list_line[1]
            if list_line[1] == '1':
                list_line[1] = '0'
            elif list_line[1] == '0':
                list_line[1] = '1'
            output_text += ' '.join(list_line) + '\n'
    with codecs.open(input_file_path[:-5] + '0.txt', 'wt') as output_file:
        output_file.write(output_text)

def expand(lstlst):
    all =[]
    for lst in lstlst:
        all.extend(lst)
    return all

def excessWordsExcluding(input_file_path, dir_path):

    excess_words_list = []
    with codecs.open(input_file_path, 'rt') as input_file:
        for line in input_file:
            line = line.lower()
            line_list = line.split()
            if line_list[1] == '1':
                excess_words_list.append(line_list[0])

    with codecs.open(input_file_path + '_', 'rt') as input_file:
        for line in input_file:
            line = line.lower()
            line_list = line.split()
            if line_list[1] == '1':
                excess_words_list.append(line_list[0])

    with codecs.open(input_file_path + '__', 'rt') as input_file:
        for line in input_file:
            line = line.lower()
            line_list = line.split()
            if line_list[1] == '1':
                excess_words_list.append(line_list[0])


    excess_words_list = list(set(excess_words_list))
    excess_words_list.sort(key = len, reverse = True)
    print excess_words_list
    with codecs.open(dir_path + "excess_words.txt", "wt") as output_file:
        output_file.write('\n'.join(excess_words_list))
        output_file.write('\n')



dir_path = './../../'
drug_names_file_path = './../../drug_names_without_NCT.txt'
drug_names_file_path_without_NCT = './../../drug_names_without_NCT.txt'
doubtful_drug_sentences_file_path = './../../doubtful_drug_sentences.txt'



#convert0To1('./../../doubtful_excess_words_manually_marked_drug-1.txt')
excessWordsExcluding('./../../doubtful_excess_words_manually_marked_drug-0', dir_path)
