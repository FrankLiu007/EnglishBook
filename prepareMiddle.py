'''
生成初中词汇表，并保存成json格式（初中词汇.json）

'''




import re
from pattern import en


if __name__=="__main__":
    f=open('初中词汇.txt', 'r', encoding='utf-8')

    status=[False, False, False]   ###记录当前的状态，必背单词？重点短语？必背句型
    is_word=False
    is_duanyu=False
    is_sentence=False
    words_list=set()
    for line in f.readlines():

        if '一、必背单词' in line:
            is_word=True
            is_duanyu = False
            is_sentence = False
        elif '二、重点短语' in line:
            is_word=False
            is_duanyu = True
            is_sentence = False
        elif  '三、必背句型' in  line:
            is_word = False
            is_duanyu = False
            is_sentence = True
        if is_word:
            words=re.findall(r'^\d{1,3}．([a-zA-Z]*).*', line)
            if not words:
                continue
            for item in words:
                words_list.add(item.lower())
        elif is_sentence:
            sentence=re.findall(r"([a-zA-Z\s,']*[\.\?!])", line)
            if not sentence:
                continue
            ll=en.parse(sentence[0], relations=True, lemmata=True).split()[0]
            for item in ll:
                words_list.add(item[-1])
        elif is_duanyu:
            ll = re.findall(r'^\d{1,3}．([a-zA-Z\s]*).*', line)
            if not ll:
                continue
            for item in ll[0].split():
                words_list.add(item.lower())

###-write to file to check
    with open('middle.txt', 'w', encoding='utf-8') as f:
        for item in words_list:
            f.write(item)
            f.write('\n')

##  write to disk
    f=open('初中词汇.json', 'w', encoding='utf-8')
    import json
    json.dump(list(words_list), f)
    f.close()
    print('len(words_list)', len(words_list))
