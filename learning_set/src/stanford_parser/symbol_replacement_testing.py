import string
import re


str_ = "@(\goor\")()/(.\'krew!?)"
p = re.compile('/|\)|\(|@|\.|!|\?')
print p.sub(' ', str_).split()

str_ = "@(\goor\")()/(.\'<krew>!?)"
rule = string.maketrans('!@#$%^&*()_=\\|<>,./?\'\"', '                      ')
print str_.translate(rule).split()