import docx
import pystardict

def get_word_list(line):
    return line.split()
def get_phonetic_translation(word):
    return 0


path='stardict-powerword2011/powerword2011_1_900'

dict=pystardict.Dictionary(path)
path='高考英语阅读.txt'
doc=docx.Document()
with open(path, 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        for word in line.split():
            break
