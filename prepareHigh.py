'''
处理高中词汇表，并存入  高中词汇.json,
暂时没处理短语

'''

import re

def get_high_vocabulary(highPath):
    word_list=[]
    previous_line=''

    previous_word_line=False

    with open(highPath, encoding='utf-8') as f:
        r = r'^(n|adj|adv|v|vi|vt|prep|pron|conj)[^a-zA-Z].*$'
        lines=f.readlines()
    for line in lines:
        line=line.strip().replace('△', '')

        if len(line)==0 or '男子名' in line or '女子名' in line or '姓氏' in line:
            continue

        if re.match(r'(Unit\s)[0-9]', line):
            continue

        if re.match(r, line) or re.match(r'^[^a-zA-Z].*$', line) :  ####是一个续行
            if previous_line=='':
                continue
            word_list.append(previous_line+line)
            previous_word_line=False
        else:
            if previous_word_line :
                word_list.append(previous_line)
            previous_line = line
            previous_word_line=True

    return word_list

def get_high_wordset(path):   ###暂时不处理短语
    word_set=set()
    with open(path,'r', encoding='utf-8') as f:
        lines=f.readlines()
    r = r'^([a-zA-Z]{1,20})[\s]{1,5}\[.*\]'
    for line in lines:
        line=line.replace('[', ' [')

        tt= re.findall(r, line)
        if tt:
            # if tt[0] in ['at', 'be', 'an', 'I', 'We', 'Set', 'man' ]:
            #     print('line=', line, 'word=', tt[0])
            word_set.add(tt[0].lower())

    return word_set

if __name__=='__main__':
    print('run main')
    highPath = '高中词汇2.txt'
    word_list=get_high_vocabulary(highPath)
    outF=open('outHigh.txt', 'w', encoding='utf-8')
    for item in word_list:
        print(item, file=outF)
    outF.close()

    word_set=get_high_wordset('outHigh.txt')
    f=open('高中词汇.json', 'w', encoding='utf-8')
    import json
    json.dump(list(word_set),f)
    f.close()