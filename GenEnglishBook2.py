import re
import pystardict
import docx
import datetime
from pattern import en
import nltk
import json


def isAlpha(str1):
    if (str1 >= 'a' and str1 <= 'z') or (str1 >= 'a' and str1 <= 'z'):
        return True
    else:
        return False


def pharseLangdao(word):
    tt = word.split('\n')
    yinbiao = ''
    fanyi = []
    for item in tt:
        kk = item.lstrip(' ')
        # print('kk=',kk, isAlpha(kk[0]))
        if isAlpha(kk[0]):
            fanyi.append(kk)
        elif kk[0] == '*':
            yinbiao = kk[1:]
        else:
            break
    return (yinbiao, ','.join(fanyi))


def pharseQuick_eng(word):
    pass


def pharseDictItem(source, item):  ##处理单个单词

    if source == '朗道':
        return pharseLangdao(item)
    elif source == '英中简明':
        return pharseQuick_eng(item)


def init_dicts():
    dict1 = ('朗道', 'stardict-langdao-ec-gb-2.4.2/langdao-ec-gb')
    dict2 = ('英中简明', 'stardict-quick_eng-zh_CN-2.4.2/quick_eng-zh_CN')
    dict_path = [dict1, dict2]
    dicts = []
    for i in range(0, len(dict_path)):
        print(dict_path)
        x = [dict_path[i][0], pystardict.Dictionary(dict_path[i][1])]
        dicts.append(x)
    return dicts


def get_local_translation(dicts, word):  ##获取音标和翻译

    for dic in dicts:
        dictItem = dic[1].get(word, 'no')
        # print('dictItem=', dictItem)
        if (dictItem != 'no'):
            return pharseDictItem(dic[0], dictItem)


## 获取英文文章的所有段落。get all paragraphs from an english reading
def get_paragraphs(path):
    with open(path, 'r', encoding='UTF-8') as f:
        paragraphs = []
        for ll in f.readlines():
            ll = ll.replace('\r', '').replace('\n', '')

            paragraphs.append(re.findall(r'([a-zA-Z][^\.\?!]*[\.\?!])', ll))

        return paragraphs


# -----------------------------------
#  处理一行的数据，可以剥离成处理一个单词的
def processSentence(dicts, sentence):
    result = []

    ll = en.parse(sentence, relations=True, lemmata=True)
    print('ll=', ll)
    for word in ll.split()[0]:
        wd = word[-1]
        if not wd.isalpha():
            result.append((word, ''))
            continue
        if wd in high_wordset:
            xx = get_translation_from_iciba(wd)
            result.append((word, xx))
        else:
            if wd in middle_wordset:
                result.append((word, ''))
            else:
                xx = get_translation_from_iciba(wd)
                result.append((word, xx))
    return result


###副词转形容词
def adverb2adject(word):
    possible_adj = []
    for ss in nltk.corpus.wordnet.synsets(word):
        for lemmas in ss.lemmas():  # all possible lemmas

            for ps in lemmas.pertainyms():  # all possible pertainyms
                possible_adj.append(ps.name())
    if 'more' in word or 'most' in word:
        return [word]
    if not possible_adj:
        return [word]
    return possible_adj


###获取单词的基本形式，包括副词转形容词
def get_basic_form(wd):
    word = wd[0]
    tag = wd[1]
    # print('wd=', wd)
    wnl = nltk.stem.WordNetLemmatizer()
    result = word
    if tag.startswith('VB'):
        result = wnl.lemmatize(word, 'v')
    elif tag.startswith("NN"):
        result = wnl.lemmatize(word, 'n')
    elif tag.startswith('JJ'):
        result = wnl.lemmatize(word, 'a')
    elif tag.startswith("R"):
        result = adverb2adject(word)[0]
    return result


###解析句子，由于pattern.en.parse不好用，错误较多，故使用nltk的，并增加副词转形容词
def parse_sentence(sentence):
    result = []
    tokens = nltk.word_tokenize(sentence)

    for word, tag in nltk.pos_tag(tokens):  ###
        bas = get_basic_form((word.lower(), tag))
        result.append((word, tag, bas.lower()))

    return result


# ----------------------------------------
def find_word_index(vocabulary, word):
    index=-1
    for dd in vocabulary:
        if word in  dd:
            index=dd[0]
    return index
###获取音标-------
def get_yinbiao(dicts, word):
    if '英' in dicts[word.lower()]['yinbiao']:
        yinbiao = dicts[word.lower()]['yinbiao']['英']
    elif 'all' in dicts[word.lower()]['yinbiao']:
        yinbiao = dicts[word.lower()]['yinbiao']['all']
    else:
        yinbiao = ''
    return  yinbiao

def processSentence2(sentence, dicts, high_words, middle_words, i,  vocabulary):
    new_sentence = []

    # vocabulary['high']=[]
    # vocabulary['extra'] = []
    print('in processSentence2, i=', i)

    ll = parse_sentence(sentence)
    # print('ll=', ll)
    for word in ll:
        basic_form = word[-1]  ####wd是单词的基础型
        this_word = word[0]  # 原单词
        word_tag = word[1]  ##词性
        # print('word=', word)
        if not isAlpha(basic_form):
            new_sentence.append(word[0])
            continue
        try:
            translation=dicts[this_word.lower()]
        except:
            print('单词：'+this_word+'  未收录！！')
            continue



        if basic_form.lower() in high_words:
            yinbiao=get_yinbiao(dicts, this_word)
            index = find_word_index(vocabulary, word)
            if index == -1:
                vocabulary.append((i, this_word.lower(), 'high', dicts[this_word.lower()] ))
                new_sentence.append(this_word + yinbiao + str(i))
                i=i+1

            else:
                new_sentence.append(this_word + yinbiao+str(index))

        elif basic_form.lower() in middle_words:
            new_sentence.append(word[0])
            continue
        else:
            yinbiao = get_yinbiao(dicts, this_word)
            index = find_word_index(vocabulary, word)
            if index==-1:
                new_sentence.append(this_word + yinbiao+str(i))
                vocabulary.append((i, this_word.lower(), 'extra',  dicts[this_word.lower()]))
                i=i+1
            else:
                new_sentence.append(this_word + yinbiao+str(index))

    return (i, new_sentence)


####-------------------main-------------------
#
# middlePath = '初中词汇.txt'
# highPath = '高中词汇(含短语).txt'
# print('begin init dictionaries:')

# ----------------Readme说明-----------------
# 当前，初中词汇1400，高中2400，其中重复400，暂时以高中词汇为参考标准音标，
# 如果有不合适的过于简单的单词，从高中词汇表中移除即可
# for word in middle_wordset:
#     if word in high_wordset:
#         print(word)
#         high_wordset.remove(word)
# -------------------------------------------------

if __name__ == "__main__":
    with open('初中词汇.json', 'r', encoding='utf-8') as f:
        middle_words = json.load(f)
    with open('高中词汇.json', 'r', encoding='utf-8') as f:
        high_words = json.load(f)

    with open('dicts_from_iciba.json', 'r', encoding='utf-8') as f:
        dicts = json.load(f)

    ###dicts太复杂，要简化一下？？？？

    # begin process readings
    path = '高考英语阅读.txt'

    paragraphs = get_paragraphs(path)

    new_paragraphs = []

    vacubulary = []


    i=1
    j=0
    for paragraph in paragraphs:
        new_paragraph=[]
        for sentence in paragraph:
            j=j+1
            print('processing sentence '+ str(j), 'i=',i)
            if len(sentence) > 0:
                result = processSentence2(sentence, dicts, high_words, middle_words, i, vacubulary)
                new_paragraph.append(result[1])
                # vacubulary['high'].extend(result[2]['high'].copy())
                # vacubulary['extra'].extend(result[2]['extra'].copy())
                i=result[0]

        new_paragraphs.append(new_paragraph.copy())
        break



#
# doc=docx.Document()
# outPath=''
# for sentence in sentences:
#     paragraphs = processSentence(sentence)
#     doc.add_paragraph(paragraphs)
#
# doc.save(outPath)
#
