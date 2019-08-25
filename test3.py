import re
#----------init high school vocabulary------------------
def get_high_wordset(path):   ###不处理短语
    word_set=set()
    with open(path,'r', encoding='utf-8') as f:
        lines=f.readlines()
    r = r'^([a-zA-Z]{1,20})[\s]{1,5}\[.*\]'
    for line in lines:
        line=line.replace('[', ' [')

        tt= re.findall(r, line)
        if tt:
            word_set.add(tt[0])
            print('tt=', tt)
    return word_set

path='高中词汇(含短语).txt'
word_list=get_high_wordset(path)

