import os
import re
import urllib2
import codecs
import string
import enchant
import random

from xml.etree import ElementTree


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

def markAllDrugFilesWithGlobalDict(input_dir_path, output_dir_path, dict_file_path):

    with codecs.open(output_dir_path + '_log.txt', 'wt') as log_file:
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        list_of_files = os.listdir(input_dir_path)
        files_count = len(list_of_files)
        marked_files_count = 0
        files_with_drugs = 0

        global_dict = []
        with codecs.open(dict_file_path, 'rt') as dict_file:
            for word in dict_file:
                global_dict.append(word[:-1])

        global_dict.sort()

        for filename in list_of_files:

            try:
                with open(input_dir_path + '/' + str(filename), 'rt') as input_text_file:
                    drug_checked_text = ''
                    drug_counter = 0

                    for line in input_text_file:
                        if line == '\n' :
                            drug_checked_text += '\n'
                            continue
                        drug_flag = False


                        word_for_check = line.split()[0].lower()
                        word_for_check = word_for_check.decode("windows-1252") #smth hack
                        word_for_check = word_for_check.encode('ascii', 'ignore')
                        rule = string.maketrans(u'!@#$%^&*()[]_=\\|<>,./?\'\":;', u'                          ')
                        word_for_check = word_for_check.translate(rule).strip()



                        if word_for_check in global_dict :
                            drug_checked_text += (line[:-1] + (" 1\n"))
                            drug_counter += 1
                            #print line
                        else:
                            drug_checked_text += (line[:-1] + (" 0\n"))


                        with open(output_dir_path + '/' + str(filename), "wt") as output_file:
                            output_file.write(drug_checked_text)

                    if drug_counter > 0:
                        files_with_drugs += 1
                    print str(drug_counter) + " drugs marked"
                    marked_files_count += 1
                    print(str(marked_files_count) + '/' + str(files_count) + ' : ' + str(filename) + ' successfully created')
                    print ''
                    log_file.write(str(marked_files_count) + '/' + str(files_count) + ' : ' + str(filename) + ' successfully created' +'\n\n')
            except Exception, e:
                print "Error: "
                print e

        print(str(files_with_drugs) + '/' + str(marked_files_count) + ' : files contain some drugs.')
        log_file.write(str(files_with_drugs) + '/' + str(marked_files_count) + ' : files contain some drugs.')

def markAllDrugFilesSmartly(input_dir_path, output_dir_path, dict_file_path):

    with codecs.open(output_dir_path + '_log.txt', 'wt') as log_file:
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        list_of_files = os.listdir(input_dir_path)
        files_count = len(list_of_files)
        marked_files_count = 0
        files_with_drugs = 0


        with codecs.open(dict_file_path, 'rt') as dict_file:
            cur_NCT = ''
            for line in dict_file:
                if line[0:3] == 'NCT':
                    cur_NCT = line[:-1]
                elif cur_NCT + '.txt' in list_of_files:
                    cur_dic = line.split()
                    print cur_NCT
                    log_file.write(cur_NCT + '\n')
                    try:
                        filename = cur_NCT + '.txt'
                        with open(input_dir_path + '/' + str(filename), 'rt') as input_text_file:
                            drug_checked_text = ''
                            drug_counter = 0

                            for line in input_text_file:
                                if line == '\n' :
                                    drug_checked_text += '\n'
                                    continue
                                drug_flag = False
                                for drug in cur_dic:
                                    #print "[" + drug.lower() + "] in [" + line.lower() + "]"

                                    word_for_check = line.split()[0].lower()


                                    word_for_check = word_for_check.decode("windows-1252") #smth hack
                                    word_for_check = word_for_check.encode('ascii', 'ignore')
                                    rule = string.maketrans(u'!@#$%^&*()[]_=\\|<>,./?\'\":;', u'                          ')
                                    word_for_check = word_for_check.translate(rule).strip()


                                    if drug == word_for_check:
                                        drug_flag = True
                                        break

                                if drug_flag:
                                    line = line[:-1] + (" 1\n")
                                    drug_counter += 1
                                    #print line
                                else:
                                    line = line[:-1] + (" 0\n")

                                drug_checked_text += line
                            with open(output_dir_path + '/' + str(filename), "wt") as output_file:
                                output_file.write(drug_checked_text)
                            if drug_counter > 0:
                                files_with_drugs += 1
                            print str(drug_counter) + " drugs marked"
                            log_file.write(str(drug_counter) + " drugs marked\n")
                            marked_files_count += 1
                            print(str(marked_files_count) + '/' + str(files_count) + ' : ' + str(filename) + ' successfully created')
                            print ''
                            log_file.write(str(marked_files_count) + '/' + str(files_count) + ' : ' + str(filename) + ' successfully created' + '\n\n')
                    except Exception, e:
                        print "Error: "
                        print e

        print(str(files_with_drugs) + '/' + str(marked_files_count) + ' : files contain some drugs.')
        log_file.write(str(files_with_drugs) + '/' + str(marked_files_count) + ' : files contain some drugs.')

#Brute solution, without filters
def markAllDrugFiles(input_dir_path, output_dir_path):

    if os.path.exists(output_dir_path + 'complited_drug_documents_with_tags'):
        os.makedirs(output_dir_path  + 'complited_drug_documents_with_tags')

    list_of_files = os.listdir(input_dir_path + 'separated_drug_documents_with_tags')
    files_count = len(list_of_files)
    marked_files_count = 0


    for filename in list_of_files:
        marked_files_count += 1
        NCT = filename[:-4]
        print(NCT)
        try:

            page = urllib2.urlopen('http://clinicaltrials.gov/show/'+NCT+'?resultsxml=true')
            document = ElementTree.parse(page)
            intervention_group = document.find('intervention/intervention_name')
            #print intervention_group.text
            drugs = intervention_group.text
            drugs = drugs.translate(None, ')(')
            print drugs
            drugs = drugs.split()

            with open(input_dir_path + 'separated_drug_documents_with_tags' + '/' + str(filename), 'rt') as input_text_file:
                drug_checked_text = ''
                drug_counter = 0

                for line in input_text_file:
                    drug_flag = False
                    for drug in drugs:
                        #print "[" + drug.lower() + "] in [" + line.lower() + "]"
                        #drug = re.sub('\)\(', '', drug)


                        if drug.lower() in line.lower().split():
                            drug_flag = True
                            break

                    if drug_flag:
                        line = line[:-1] + (" 1\n")
                        drug_counter += 1
                        #print line
                    else:
                        line = line[:-1] + (" 0\n")

                    drug_checked_text += line
                with open(output_dir_path + 'complited_drug_documents_with_tags' + '/' + str(filename), "wt") as output_file:
                    output_file.write(drug_checked_text)
                print str(drug_counter) + " drugs marked"
                print(str(marked_files_count) + '/' + str(files_count) + ' : ' + str(filename) + ' successfully created')
                print ''


        except Exception, e:
            print "Error: "
            print e





dir_path = './../../'



#markAllDrugFilesSmartly(dir_path + 'separated_drug_documents_with_tags', dir_path  + 'complited_drug_documents_with_tags_filtered', './../../drug_names_with_NCT_filtered.txt')
#filesMerger(dir_path + 'complited_drug_documents_with_tags_filtered', dir_path + 'complited_drug_documents_with_tags_filtered.txt')

markAllDrugFilesWithGlobalDict(dir_path + 'separated_drug_documents_with_tags', dir_path  + 'complited_drug_documents_with_tags_global_dict', './../../drug_dictionary_for_all_NCT.txt')
filesMerger(dir_path + 'complited_drug_documents_with_tags_global_dict', dir_path + 'complited_drug_documents_with_tags_global_dict.txt')


#filesMerger(dir_path + 'separated_drug_documents', dir_path + "drug_docs")
#markAllDrugFiles(dir_path, dir_path)