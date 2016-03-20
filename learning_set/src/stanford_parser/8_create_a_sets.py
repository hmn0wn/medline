import subprocess
from datetime import datetime
import string
import random
import os, sys

def lenOfFile(input_file_path):
    with open(input_file_path) as f:
       return len(list(f))

def hideDrugWords(input_file_path):
    with open(input_file_path , 'rt') as input_text_file:
        with open(input_file_path + "_drug_hiden" , 'wt') as output_text_file:
            for line in input_text_file:
                if line == '\n':
                    #print line
                    output_text_file.write(line)
                    continue

                line_list = line.split()

                if line_list[2] == "1":
                    line_list[0] = str(random.randint(1, 65536))
                    line = ' '.join(line_list) + "\n"
                #print line
                output_text_file.write(line)

def sentencesParse(input_file_path):
    with open(input_file_path , 'rt') as input_text_file:
        sentences = []
        sentence = []
        for line in input_text_file:
            if line != "\n":
                sentence.append(line)
            else:
                sentences.append(list(sentence))
                sentence = []
        return sentences

def createSets(crf_dir_path, input_file_path):
    random_flag = 0
    time = str(datetime.now())
    rule = string.maketrans(u' .\\/:*?\'\"<>|', u'____________')
    name = time.translate(rule)
    print name + "_train.data"
    print name + "_test.data"


    sentences = sentencesParse(input_file_path)
    numbers = range(0, len(sentences))
    #print numbers
    if random_flag :
        random.shuffle(numbers)
    #print numbers

    train_ratio = 0.7
    train_count = int(len(sentences) * train_ratio)
    name = name + "_tr=" + str(int(train_ratio * 100))
    if random_flag:
        name = name + "_random"

    result_path = crf_dir_path + "logs/results/" + name +"_result.log"
    with open(result_path, 'a') as test_log_file:
         test_log_file.write(str(random_flag) + "\n")
         test_log_file.write(str(train_ratio) + "\n")

    with open(crf_dir_path + "trains/" + name + "_train.data", 'wt') as train_text_file:
        for i in range(0, train_count - 1):
            for line in sentences[i]:
                train_text_file.write(line)
            train_text_file.write("\n")

    with open(crf_dir_path + "tests/" + name + "_test.data", 'wt') as train_text_file:
        for i in range(train_count, len(sentences)):
            for line in sentences[i]:
                train_text_file.write(line)
            train_text_file.write("\n")

    hideDrugWords(crf_dir_path + "tests/" + name + "_test.data")
    os.rename(crf_dir_path + "tests/" + name + "_test.data", crf_dir_path + "tests/" + name + "_test_not_hiden.data")
    os.rename(crf_dir_path + "tests/" + name + "_test.data_drug_hiden", crf_dir_path + "tests/" + name + "_test.data")
    return name

def testLogAnalise(crf_dir_path, name):

    test_log_path = crf_dir_path + "logs/tests/" + name +"_test.log"
    with open(test_log_path, 'rt') as test_log_file:
        #positive/negative - classif answer words[3]
        #true/false        - this answer's honesty

        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        count = 0

        for line in test_log_file:
            try:
                words = line.split()
                #print words
                if not(len(words) == 1 or len(words) == 4):
                    continue
                count = count + 1
                if(words[3] == "1"):
                    if(words[2] =="1"):
                        true_positive += 1
                    else:
                        false_positive += 1
                else:
                    if(words[2] =="1"):
                        false_negative += 1
                    else:
                        true_negative += 1
            except Exception:
                print " error in " + str(count)
                print line
                continue

        precision = true_positive /(true_positive + false_positive + .0)
        recall = true_positive /(true_positive + false_negative + .0)

        print "\n" + name + "_test.log"
        print "TP       \t=\t" + str(true_positive)
        print "TN       \t=\t" + str(true_negative)
        print "FP       \t=\t" + str(false_positive)
        print "FN       \t=\t" + str(false_negative)
        print "sum      \t=\t" + str(true_negative + true_positive + false_negative + false_positive)
        print "count    \t=\t" + str(count)
        print "precision\t=\t" + str(precision)
        print "recall   \t=\t" + str(recall)


        result_path = crf_dir_path + "logs/results/" + name +"_result.log"
        with open(result_path, 'a') as test_log_file:

            test_log_file.write(str(true_positive) + "\n")
            test_log_file.write(str(true_negative) + "\n")
            test_log_file.write(str(false_positive) + "\n")
            test_log_file.write(str(false_negative) + "\n")
            test_log_file.write(str(count) + "\n")
            test_log_file.write(str(precision) + "\n")
            test_log_file.write(str(recall) + "\n")

def dicAnalise(crf_dir_path, name):
    test_log_path = crf_dir_path + "tests/" + name +"_test_not_hiden.data"

    drugs_dict_test = {}

    with open(test_log_path, 'rt') as test_data_file:
        count = 0
        for line in test_data_file:
            try:
                count += 1
                words = line.split()
                drug = ""

                if not(len(words) == 1 or len(words) == 3):
                    continue

                if(words[2] == "1"):
                    drug = words[0]
                    if drug in drugs_dict_test:
                        drugs_dict_test[drug] += 1
                    else:
                        drugs_dict_test.update({drug : 1})


            except Exception:
                print " error in " + str(count)
                print line
                continue

    train_log_path = crf_dir_path + "trains/" + name +"_train.data"

    drugs_dict_train = {}

    with open(train_log_path, 'rt') as train_data_file:
        count = 0
        for line in train_data_file:
            try:
                count += 1
                words = line.split()
                drug = ""

                if not(len(words) == 1 or len(words) == 3):
                    continue

                if(words[2] == "1"):
                    drug = words[0]
                    if drug in drugs_dict_train:
                        drugs_dict_train[drug] += 1
                    else:
                        drugs_dict_train.update({drug: 1})

            except Exception:
                print " error in " + str(count)
                print line
                continue

    sim_test_drug_count = 0
    test_count = 0
    train_count = 0

    for train_drug in drugs_dict_train:
        train_count += drugs_dict_train[train_drug]

    for test_drug in drugs_dict_test:
        test_count += drugs_dict_test[test_drug]
        if test_drug in drugs_dict_train:
            sim_test_drug_count += drugs_dict_test[test_drug]

    result_path = crf_dir_path + "logs/results/" + name +"_result.log"

    uniq_qrug = (test_count - sim_test_drug_count + .0)/test_count
    with open(result_path, 'at') as log_file:
        log_file.write(str(test_count) + "\n")
        log_file.write(str(train_count) + "\n")
        log_file.write(str(sim_test_drug_count) + "\n")
        log_file.write(str(uniq_qrug) + "\n")


    print "test_count    \t=\t" + str(test_count)
    print "train_count   \t=\t" + str(train_count)
    print "sim_drug_count\t=\t" + str(sim_test_drug_count)
    print "uniq_qrug     \t=\t" + str(uniq_qrug)

def createModellAndTest(crf_dir_path, input_file_path):
    name = createSets(crf_dir_path, input_file_path)

    train_command =   crf_dir_path + "crf_learn -c 10.0 -p 2 " \
                    + crf_dir_path + "templates/template " \
                    + crf_dir_path + "trains/" + name +"_train.data " \
                    + crf_dir_path + "models/" + name + "_model"

    # train_command =   crf_dir_path + "crf_learn -a MIRA " \
    #             + crf_dir_path + "templates/template " \
    #             + crf_dir_path + "trains/" + name +"_train.data " \
    #             + crf_dir_path + "models/" + name + "_model"

    print train_command
    train_log_path = crf_dir_path + "logs/trains/" + name +"_train.log"

    p = subprocess.Popen(train_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with open(train_log_path, 'wt') as train_log_file:
        for line in p.stdout.readlines():
            print line,
            train_log_file.write(line)
    retval = p.wait()

    test_command =   crf_dir_path + "crf_test -m " \
                   + crf_dir_path + "models/" + name + "_model " \
                   + crf_dir_path + "tests/" + name + "_test.data"

    test_log_path = crf_dir_path + "logs/tests/" + name +"_test.log"

    p = subprocess.Popen(test_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with open(test_log_path, 'wt') as test_log_file:
        for line in p.stdout.readlines():
            print line,
            test_log_file.write(line)
    retval = p.wait()

    testLogAnalise(crf_dir_path, name)
    dicAnalise(crf_dir_path, name)
    faqToLogRes(crf_dir_path, name)

def faqToLogRes(crf_dir_path, name):
        result_path = crf_dir_path + "logs/results/" + name +"_result.log"
        with open(result_path, 'a') as test_log_file:
            test_log_file.write("\n\n#F.A.Q.\n")
            test_log_file.write("---------------\n")
            test_log_file.write("#Random flag\n")
            test_log_file.write("#Train ratio\n")
            test_log_file.write("#True Positive\n")
            test_log_file.write("#True Negative\n")
            test_log_file.write("#False Positive\n")
            test_log_file.write("#False Negative\n")
            test_log_file.write("#Count of test set\n")
            test_log_file.write("#Precision\n")
            test_log_file.write("#Recall\n")
            test_log_file.write("#Drug count in test set\n")
            test_log_file.write("#Drug count in train set\n")
            test_log_file.write("#Drug count in test set(sim train dic)\n")
            test_log_file.write("#Uniq drug count in test set\n")


            test_log_file.write("\n\n#Positive/Negative - classif answer, the 4th column in *_test.log")
            test_log_file.write("\n#True/False        - this answer's honesty")

#Linux
dir_path = './../../'
crf_dir_path = dir_path + "crf/"
data_path = dir_path + 'complited_drug_documents_with_tags_global_dict.txt'

#Windows
# dir_path = '.\..\..\\'
# crf_dir_path = dir_path + "crf\\"
# data_path = dir_path + 'complited_drug_documents_with_tags_global_dict.txt'

#hideDrugWords(data_path)
#print lenOfFile(data_path)
#sentencesParse(data_path)
#createSets(dir_path + "sets/", data_path)
createModellAndTest(crf_dir_path, data_path)
#dicAnalise(crf_dir_path, "2016-03-04_19_45_49_566923_tr=70")
#testLogAnalise(crf_dir_path, "2016-02-24_00:37:53.307964")