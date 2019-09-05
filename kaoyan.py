import glob
import docx
from WordFrequence import count_word_frequence
if __name__=="__main__":
    dir0 = '考研英语二'
    path_list = glob.glob(dir0 + '/*.docx')
    docs = []
    for p in path_list:
        if '$' in p:  ###略过临时文件
            continue
        doc = docx.Document(p)
        docs.append(doc)


    words_all = count_word_frequence(docs)
    import json
    with open('kaoyan_words.json', 'w', encoding='utf-8') as f:
        json.dump(words_all, f)