import re
import pystardict
import docx
from docx.shared import Pt
import datetime
import  difflib
from pattern import en
# from dicts import get_translation_from_iciba
# from word_forms.word_forms import get_word_forms
# maxNumber= 60
#
# middle_wordList = []
# senior_wordList = []
# note_list = []
high_word_list=dict()

middle_word_list=dict()

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

def get_local_translation( dicts, word):  ##获取音标和翻译

    for dic in dicts:
        dictItem = dic[1].get(word , 'no')
        # print('dictItem=', dictItem)
        if(dictItem!='no'):
            return pharseDictItem(dic[0] ,dictItem)

##判断是否英文单词
def is_word(word):
    from nltk.corpus import wordnet

    if  wordnet.synsets(word):
        return True
    else:
        return False


## 获取英文文章的所有段落。get all paragraphs from an english reading
def get_paragraphs(path):
    with open(path, 'r', encoding='UTF-8') as f :
        paragraphs=[]
        for ll in f.readlines():
            ll=ll.replace('\r', '').replace('\n', '')
            paragraphs.append( re.findall(r'([a-zA-Z][^\.\?!]*[\.\?!])', ll) )
        return  paragraphs
#-----------------------------
#  处理一行的数据，可以剥离成处理一个单词的

def processSentence( sentence,high_wordlist, middle_wordlist ):
    result=set()
    ll = en.parse(sentence, relations=True, lemmata=True)
    print('ll=', ll)
    for word in ll.split()[0]:
        if not is_word(word[0]):
            continue
        wd=word[-1]
        result.add(wd)
    return result
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



####-------------------main-------------------
if __name__=="__main__":

## step1. 读取crawl_dicts 生成的json格式的所有单词数据，得到所有的单词频率
    f=open('all_words.json', 'r', encoding='utf-8')
    import json
    words_all=json.load(f)
    f.close()

##step2. 把在 a.高中词汇表中的单词  b. 不在高中词汇表，但也不在初中词汇表的单词  取出来

    print('begin init dictionaries:')
    # dicts = init_dicts()

    #读取初中词汇
    f=open('初中词汇.json', 'r', encoding='utf-8')
    middle_wordlist = json.load(f)
    f.close()
    ##读取高中词汇
    f = open('高中词汇.json', 'r', encoding='utf-8')
    high_wordlist = json.load(f)
    f.close()

    # words_hi={}
    # words_extra={}
    # for word in words_all:
    #     if word in high_wordlist:
    #         words_hi[word]=words_all[word]
    #     else:
    #         if word in middle_wordlist:
    #             continue
    #         else:
    #             words_extra[word]=words_all[word]

    # ----------------Readme说明-----------------
    # 当前，初中词汇1400，高中2400，其中重复400，暂时以高中词汇为参考标准音标，
    # 如果有不合适的过于简单的单词，从高中词汇表中移除即可
    # for word in middle_wordset:
    #     if word in high_wordset:
    #         print(word)
    #         high_wordset.remove(word)
    # -------------------------------------------------

    # begin process readings
    path = '高考英语阅读.txt'

    paragraphs = get_paragraphs(path)
###-----1篇阅读，首先找到需要注音的单词

    result = dict()
    result["high"] = set()
    result["extra"] = set()

    for paragraph in paragraphs:

        for sentence in paragraph:
            if len(sentence) > 0:
                zz = processSentence( sentence, high_wordlist, middle_wordlist)
                result["high"]=result["high"].union(zz['high'])
                result["extra"]=result["extra"].union(zz['extra'])


    #
    # doc=docx.Document()
    # outPath=''
    # for sentence in sentences:
    #     paragraphs = processSentence(sentence)
    #     doc.add_paragraph(paragraphs)
    #
    # doc.save(outPath)
    #


