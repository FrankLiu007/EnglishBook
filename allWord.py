from word_forms.word_forms import get_word_forms
path = '词汇.txt'
wordList = []
DicList = []

with open(path, 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        for word in line.split():
            wordList.append(word)


for item in wordList:
    res = get_word_forms(item)
    temp = res['n'].union(res['r']).union(res['a']).union(res['v'])
    temp = list(temp)
    if(item in temp):
        temp.remove(item)
    temp.insert(0,item)
    DicList.append(temp)


print(DicList)

