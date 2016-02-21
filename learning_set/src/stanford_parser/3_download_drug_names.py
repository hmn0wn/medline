
import os
import re
import urllib2
import codecs
import string
import enchant

from xml.etree import ElementTree


def drugNamesDownload(input_dir_path, output_dir_path):

    list_of_files = os.listdir(input_dir_path)
    files_count = len(list_of_files)
    downloaded = 0
    errors = 0

    drugs_text = ""
    with codecs.open(output_dir_path + "drug_names_without_NCT.txt", 'wt', 'utf-8') as output_file_for_analysis:
        with codecs.open(output_dir_path + "drug_names_with_NCT.txt", 'wt', 'utf-8') as output_file:

            for filename in list_of_files:

                NCT = filename[:-4]
                print(NCT)
                try:
                    page = urllib2.urlopen('http://clinicaltrials.gov/show/'+NCT+'?resultsxml=true')
                    document = ElementTree.parse(page)
                    intervention_group = document.find('intervention/intervention_name')
                    drugs = intervention_group.text

                    output_file.write(NCT + '\n' + drugs +'\n')
                    output_file_for_analysis.write(drugs +'\n')
                    downloaded += 1
                    print str(downloaded) + " drug names downloaded and succesfully written."

                except Exception, e:
                    errors += 1
                    print "Error in " + NCT
                    print e



    print "\n\nDrugs lists succesfully downloaded:"
    print str(downloaded) + "/" + str(files_count)
    print "with " + str(errors) + " errors."

dir_path = './../../'

drugNamesDownload(dir_path + 'separated_drug_documents_with_tags', dir_path)
