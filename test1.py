import docx
import pystardict
import difflib
import heapq
import re       # 引入正则
from nltk.corpus import wordnet as wn

path1 = 'stardict-langdao-ec-gb-2.4.2/langdao-ec-gb'
path2 = 'stardict-quick_eng-zh_CN-2.4.2/quick_eng-zh_CN'

dict1 = pystardict.Dictionary(path1)
dict2 = pystardict.Dictionary(path2)

class Temp:
    pass

def get_equal_rate(str1, str2):   # 判断相似度
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def get_word_list(line):
    return line.split()
def get_phonetic_translation(word):
    return 0

def get_str_btw(s, f, b):
    par = s.partition(f)
    return (par[2].partition(b))[0][:]

def find_words(item):
    findItem = dict1.get(item , 'no')
    if(findItem != 'no'):
        findItem = findItem.split('\n')
        return findItem
    else:
        findItem = dict2.get(item , 'no')
        if(findItem != 'no'):
            findItem = findItem.split('\n')
            return findItem
        else:
            return []

# 通过wordnet获取查不到的单词
def get_words(one):
    wordList = []
    similarList = []
    # TODO 获取WordNet中的同义词集
    synsets = wn.synsets(one)  # word所在的词集列表
    for synset in synsets:
        words = synset.lemma_names()
        for oneWord in words:
            wordoneWord = oneWord.replace('_', ' ')
            wordList.append(oneWord)
    
    for item in wordList:
        if(item == one):
            similar = 0
        else:
            similar = get_equal_rate(one , item)
        similarList.append(similar)
  
    maxSimilar  = heapq.nlargest(1, similarList)
    maxSimilarIndex = similarList.index(maxSimilar[0])

    return wordList[maxSimilarIndex]

def split_Data(oneitem):
    if('相关词组:' in oneitem):
        lastIndex = oneitem.index('相关词组:')
        oneitem = oneitem[:lastIndex]
    return oneitem

# 储存数据
def keep_Data(obj , item):
    obj.say = item[0]
    obj.mean = []
    for i in range(1 , len(item)):
        matchReg = re.match(r'^【' , item[i])
        # print(matchReg) # matchReg 为none的时候，匹配不成功，没有【
        if( matchReg ):
            break
        else:
            mean = item[i]
            obj.mean.append(mean)
    return obj

# 查询过程
def query_Process(item , temp):
    one = find_words(item)
    if(len(one)<=0):
        item = get_words(item)
        temp.pro = item
        one = find_words(item)
        one = split_Data(one)
        if('*' in one[0]):
            return one
        else:
            one.insert(0, '')
            return one
    else:
        one = split_Data(one)
        flag = '*' in one[0]
        if(bool(1-flag)):
            item = get_words(item)
            temp.pro = item
            one = find_words(item)
            one = split_Data(one)
            if('*' in one[0]):
                return one
            else:
                one.insert(0, '')
                return one
        else:
            return one



path='高考英语阅读.txt'
path2 = '词汇.txt'
doc=docx.Document()
list = []
findList = []   # 查询词汇总结
articalList = []       # 文章中每个单词
wordList = []   # 词汇表

with open(path2, 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        for word in line.split():
            wordList.append(word)

with open(path, 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        for word in line.split():
            print(word , '133')
            temp = Temp()
            temp.showWord = word
            word = word.lower()
            word = re.sub(re.compile(r'[^a-zA-Z]'),"",word)
            temp.word = word
            temp.pro = word
            wordFlag = word in wordList
            
            if word in wordList:    # 如果词汇表中包含词汇就需要去查询
                print(word , '141')
                if(len(articalList)>0):            
                    for i in articalList:
                        if(i.word == word):
                            articalList.append(i)
                        else:
                            one = query_Process(word , temp)
                            keep_Data(temp , one)
                else:
                    one = query_Process(word , temp)
                    keep_Data(temp , one)    
            else:
                word = get_words(word)

            articalList.append(temp)


for item in articalList:
    print(item.word , '158')
    print(item.say , '158')



# str1 = ' '.join(list)
# doc.add_paragraph(str1)


# doc.save('test1.docx')