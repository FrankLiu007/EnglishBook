

import re
import nltk
from nltk.corpus import wordnet

if not wordnet.synsets('word_to_test'):
  print('not')
else:
    print('yes!')
f=open('初中词汇.txt', 'r', encoding='utf-8')
mm=set()
for line in f.readlines():
    for word in re.split(r'[．\s\?]', line):
        if word.isalpha():
            mm.add(word)