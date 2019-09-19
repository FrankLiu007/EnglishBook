import re
from crawl_dicts import get_translation_from_iciba
def isEnglishWord(word):
   if  re.match(r'^[a-zA-Z][a-zA-Z\-]*[a-zA-Z]$', word):
       return True
   else:
       if word=='I' or word=='a':
           return True
       else:
            return False

import  json
with open('dicts_from_iciba.json', 'r', encoding='utf-8') as f:
    dicts = json.load(f)

with open('all_words.json', 'r', encoding='utf-8') as f:
    import json
    words_all=json.load(f)

x=0
a=0

need_delete=[]
need_update=[]
for word in dicts:
    if not isEnglishWord(word):
        need_delete.append(word)
        x=x+1
        continue

    if dicts[word]['translation']=={}:
        print('word=',word)
        need_update.append(word)
        tt=get_translation_from_iciba(word)
        print('tt=', tt)
        dicts[word]=tt
        a=a+1

for item in need_delete:
    dicts.pop(item)
y=0
for word in words_all:
    if not word in dicts:
        need_update.append(word)
        tt = get_translation_from_iciba(word)
        print('tt=', tt)
        dicts[word] = tt
        y=y+1



# t_obj=[]
# import  threading
# for i in range(0,4):
#     t=threading.Thread(target=crawl_dict, args=(words_set, words_dict, i))
#     t.start()
#     t_obj.append(t)
#
# for t in t_obj:
#     t.join()
# print('crawler ends')