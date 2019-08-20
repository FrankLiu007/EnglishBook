import re
import pystardict
from word_forms.word_forms import get_word_forms
import docx
import datetime

word_list=dict()
word_package=dict()

def isAlpha(str1):
    if (str1>='a' and str1<='z' ) or  (str1>='a' and str1<='z'):
        return  True
    else:
        return False

def pharseLangdao(word):
    tt=word.split('\n')
    yinbiao=''
    fanyi=[]
    for item in tt:
        kk=item.lstrip(' ')
        # print('kk=',kk, isAlpha(kk[0]))
        if isAlpha(kk[0]):
            fanyi.append(kk)
        elif kk[0]=='*':
            yinbiao=kk[1:]
        else:
            break
    return (yinbiao, ','.join(fanyi))

def pharseQuick_eng(word):
    pass

def pharseDictItem( source ,item):  ##处理单个单词

    if source=='朗道':
        return pharseLangdao(item)
    elif source=='英中简明':
        return pharseQuick_eng(item)



def init_dicts():
    dict1 =( '朗道' ,'stardict-langdao-ec-gb-2.4.2/langdao-ec-gb')
    dict2 =('英中简明','stardict-quick_eng-zh_CN-2.4.2/quick_eng-zh_CN' )
    dict_path = [dict1, dict2]
    dicts=[]
    for i in range(0,len(dict_path)):
        x=[ dict_path[i][0], pystardict.Dictionary(dict_path[i][1])]
        dicts.append(x)
    return dicts

def get_yinbiao_fanyi( dicts, word):  ##获取音标和翻译

    for dic in dicts:
        dictItem = dic[1].get(word , 'no')
        # print('dictItem=', dictItem)
        if(dictItem!='no'):
            return pharseDictItem(dic[0] ,dictItem)


def gen_word_package(word):
    ll=get_word_forms(word)

    return ll

def removeTag(word):
    tags=[',', '.', '!', '?', ':', '-']
    for tag in tags:
        if tag in word:
            word=word.replace(tag, '')
    return word


def processLine(line):
    for word in line.split():
        w2 = word
        w2=removeTag(w2)
        w2=w2.lower()
        dd=get_word_info(w2)
        print('word=', w2, dd)




def get_word_info(word):
    if word in word_list:
        return (word, word_list[word])
    else:
        wb=find_in_wordPackage(word)
        if wb:
            return (wb, word_list[wb])

def find_in_wordPackage(word):
    for item in word_package:
        for att in word_package[item]:
            if word in word_package[item][att] :
                return item
    return None
####-------------------main-------------------
wordPath = '词汇.txt'


t1=datetime.datetime.now()
print('t1=', t1)
dicts=init_dicts()
t2=datetime.datetime.now()
print('花的时间:', (t2-t1).seconds)
print('t2=', t2)

with open(wordPath, 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        for word in line.split():
            x=get_yinbiao_fanyi( dicts, word)
            word_list[word]=x
            y=gen_word_package(word)
            word_package[word]=y

##begin process readings
path='高考英语阅读.txt'
with open(path, 'r', encoding='UTF-8') as f :
    tt=[]
    for ll in f.readlines():
        tt.append(ll)
    contents=''.join(tt)
    xx=contents.replace('\r', '').replace('\n', '')
    lines=xx.split('.')
    for line in lines:
        processLine(line)
        exit()

