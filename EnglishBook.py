import re
import pystardict
from word_forms.word_forms import get_word_forms
import docx
from docx.shared import Pt
import datetime
import  difflib
from pattern import en
from Clawer_tmp import lookup_word_all
# maxNumber= 60
#
# middle_wordList = []
# senior_wordList = []
# note_list = []
high_word_list=dict()
high_word_package=dict()

middle_word_list=dict()
middle_word_package=dict()


# def is_check_word(word):
#     for item in word_list:
#         if(word == item):
#             return (word , word_list[item])
#     if word not in middle_wordList:
#         return get_word_info(word)

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
        print(dict_path)
        x=[ dict_path[i][0], pystardict.Dictionary(dict_path[i][1])]
        dicts.append(x)
    return dicts

def get_yinbiao_fanyi( dicts, word):  ##获取音标和翻译

    for dic in dicts:
        dictItem = dic[1].get(word , 'no')
        print('dictItem=', dictItem)
        if(dictItem!='no'):
            return pharseDictItem(dic[0] ,dictItem)

def removeTag(word):
    tags=[',', '.', '!', '?', ':', '-']
    for tag in tags:
        if tag in word:
            word=word.replace(tag, '')
    return word
#-------------get basic form of a word--------------------------------
def search_in_wordPackage(package,word):
    words=[]
    if word in package:
        return word
    for item in package:
        for att in package[item]:
            if word in package[item][att] :
                words.append(item)

    return None

# def screen_word(word):
#     typeList = ['v' , 'n' , 'adj' , 'adv' , 'phr.' , 'pron' , 'prep' ]
#     for type in typeList:
#         if (word == type):
#             return 'false'
#     if(re.match(r'^[^a-zA-Z]' , word)):
#         return 'false'
#     return 'true'

###-------------------------------------------
def get_sentences(path):
    with open(path, 'r', encoding='UTF-8') as f :
        tt=[]
        for ll in f.readlines():
            tt.append(ll)
        contents=''.join(tt)
        xx=contents.replace('\r', '').replace('\n', '')
        sentences=xx.split('.')
        return  sentences
# def intersection(obj1 , obj2):
#--------------------------------
def get_word_set(path):
    word_set=set()
    with open(path, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            for word in line.split():
                word = word.lower()
                word_set.add(word)
    return word_set
##------------init middle school vocabulary-------------------
def get_middle_wordset(path):
    word_set=set()
    with open(path,'r', encoding='utf-8') as f:
        for line in f.readlines():
            tt=re.findall(r'^\d{1,5}．([a-zA-Z]{1,10}).*$', line)
            if tt:
                word_set.add(tt[0].lower())

    return word_set
#----------init high school vocabulary------------------
def get_high_wordset(path):   ###暂时不处理短语
    word_set=set()
    with open(path,'r', encoding='utf-8') as f:
        lines=f.readlines()
    r = r'^([a-zA-Z]{1,20})[\s]{1,5}\[.*\]'
    for line in lines:
        line=line.replace('[', ' [')

        tt= re.findall(r, line)
        if tt:
            if tt[0] in ['at', 'be', 'an', 'I', 'We', 'Set', 'man' ]:
                print('line=', line, 'word=', tt[0])
            word_set.add(tt[0].lower())

    return word_set
#-----------------------------------
#  处理一行的数据，可以剥离成处理一个单词的
def processSentence(dicts, sentence):
    result=[]

    ll = en.parse(sentence, relations=True, lemmata=True)
    for word in ll.split()[0]:
        wd=word[-1]
        if wd in high_wordset:
            xx = get_yinbiao_fanyi(dicts, wd)
            result.append((word, xx))
        else:
            if wd in middle_wordset:
                result.append((word, ''))
            else:
                xx = get_yinbiao_fanyi(dicts, wd)
                result.append((word, xx))
#-------------found better solutions----------------------------------
    # for word in re.split('[.,!?\s]', sentence):
    #     if word=='':
    #         continue
    #     word=word.lower()
    #
    #     dd = search_in_wordPackage(high_word_package, word)
    #     ee = search_in_wordPackage(middle_word_package, word)
    #     if ee != None:  ##word in middle wordset, ignore
    #         continue
    #     print('dd=', dd, 'word=', word)
    #     if dd!=None:  ####  word is in high wordset
    #         xx=get_yinbiao_fanyi(dicts, dd)
    #         result.append( (word,xx) )
    #     else:
    #         xx = get_yinbiao_fanyi(dicts, word)
    #         result.append((word, xx))

    return result

#-----------------------------

def words2paragraph(words):
    pass
def get_word_package(word_list):
    word_package=dict()
    for word in word_list:
        word_package[word] = get_word_forms(word)
    return word_package

####-------------------main-------------------


middlePath = '初中词汇.txt'
highPath = '高中词汇(含短语).txt'
print('begin init dictionaries:')
dicts=init_dicts()

print('generate middle and high school wordset')
middle_wordset=get_middle_wordset(middlePath)
high_wordset=get_high_wordset(highPath)

print('generate middle and high school package')
middle_word_package=get_word_package(middle_wordset)  ###获取该单词所有的其它形式
high_word_package=get_word_package(high_wordset)

#----------------Readme说明-----------------
#当前，初中词汇1400，高中2400，其中重复400，暂时以高中词汇为参考标准音标，
# 如果有不合适的过于简单的单词，从高中词汇表中移除即可
#for word in middle_wordset:
#     if word in high_wordset:
#         print(word)
#         high_wordset.remove(word)
#-------------------------------------------------


#begin process readings
path='高考英语阅读.txt'

sentences=get_sentences(path)

for sentence in sentences:
    result = processSentence(dicts, sentence)
    for tt in result:
        print(tt)


#
# doc=docx.Document()
# outPath=''
# for sentence in sentences:
#     paragraphs = processSentence(sentence)
#     doc.add_paragraph(paragraphs)
#
# doc.save(outPath)
#


