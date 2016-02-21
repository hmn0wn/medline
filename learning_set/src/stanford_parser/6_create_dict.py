
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
    with codecs.open(input_file_path + '_reversed', 'wt') as output_file:
        output_file.write(output_text)

def expand(lstlst):
    all =[]
    for lst in lstlst:
        all.extend(lst)
    return all

def filesMerger(dir_path, result_file_path):
    list_of_files = os.listdir(dir_path)
    with codecs.open(result_file_path, 'wr') as output_file:
        for file_name in list_of_files:
            with codecs.open(dir_path + '/' + file_name) as input_file:
                all_text = input_file.read()

                output_file.write(all_text)




def createPerfectDict(current_dict_path, excess_words_path, dir_path):

    excess_words_list = []
    with codecs.open(excess_words_path, "rt") as excess_words_fle:
        for word in excess_words_fle:
            excess_words_list.append(word[:-1])

    output_counter = 0
    dict_for_all_NCT = []
    with codecs.open(current_dict_path, "rt") as current_dict_file:
        with codecs.open(current_dict_path[:-4] + "_filtered.txt", "wt") as filtered_dict_file:
            curent_NCT = ''
            for line in current_dict_file:
                if line[0:3] == 'NCT':
                    curent_NCT = line
                    #filtered_dict_file.write(line)
                else:
                    pass
                    #if curent_NCT[:-1] in empty_NCT:
                    #    print line[:-1]

                    line = line.lower()
                    line = line.decode("windows-1252") #smth hack
                    line = line.encode('ascii', 'ignore')
                    rule = string.maketrans(u'!@#$%^&*()[]_=\\|<>,./?\'\":;', u'                          ')
                    line_list = line.translate(rule).split()

                    filtered_line_list = []
                    for word in line_list:
                        if isint(word):
                            continue
                        if word in excess_words_list:
                            continue
                        else:
                            filtered_line_list.append(word)

                    if len(filtered_line_list) == 0:
                        pass
                        #print '\'' + curent_NCT[:-1] + '\','
                    else:
                        output_counter += 1
                        dict_for_all_NCT.append(filtered_line_list)
                        filtered_dict_file.write(curent_NCT)
                        filtered_dict_file.write(' '.join(filtered_line_list) + '\n')

    dict_for_all_NCT =  expand(dict_for_all_NCT)
    dict_for_all_NCT = list(set(dict_for_all_NCT))
    dict_for_all_NCT.sort(key = len, reverse = True)

    with codecs.open(dir_path + 'drug_dictionary_for_all_NCT.txt', 'wt') as output_file:
        output_file.write('\n'.join(dict_for_all_NCT))
        output_file.write('\n')


    print("\nDict of all NCT saccesfully created")
    print(str(output_counter) + " miniDict for each NCT not empty")

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


createPerfectDict(dir_path + 'drug_names_with_NCT.txt', dir_path + 'excess_words.txt', dir_path)

