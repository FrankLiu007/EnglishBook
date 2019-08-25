
from pattern import en

def get_sentences(path):
    with open(path, 'r', encoding='UTF-8') as f :
        tt=[]
        for ll in f.readlines():
            tt.append(ll)
        contents=''.join(tt)
        xx=contents.replace('\r', '').replace('\n', '')
        sentences=xx.split('.')
        return  sentences
path='高考英语阅读.txt'

sentences=get_sentences(path)
tt=[]
for sentence in sentences:
    # paragraphs = processSentence(sentence)
    # for tt in paragraphs:
    #     print(tt)
    # exit()
    print('sentence:\n', sentence)
    ll=en.parse(sentence, relations=True, lemmata=True)
    tt.append(ll)
    print(ll)