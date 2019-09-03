import requests
import re
import bs4
from WordFrequence import *


def get_translation_from_iciba(word):
    words_dict = {}
    words_alp = {}
    words_sound = {}
    word_website = 'http://www.iciba.com/' + word
    res = requests.get(word_website)
    soup = bs4.BeautifulSoup(res.text,"lxml")
    word_sounds = soup.select('i[class="new-speak-step"]')
    word_alps = soup.select('div[class="base-speak"] span span')
    word_means = soup.select('li[class="clearfix"]')
    pattern = "sound\('(.*)'\)"
    for i, word_sound in enumerate(word_sounds):
        # print(word_sound)
        line = str(word_sound.get("ms-on-mouseover"))
        re_res = re.match(pattern,line)
        sound_url = re_res[1]
        if i == 0:
            words_sound["英"] = sound_url
        else:
            words_sound["美"] = sound_url
    # print(words_sound)
    for alp in word_alps:
        str_alp = str(alp.getText())
        alp_info = str_alp.split(" ")
        words_alp[alp_info[0]] = alp_info[1]
    # print(words_alp)
    for each_property_mean in word_means:
        word_property = each_property_mean.select('span[class="prop"]')[0].get_text()
        pep_word_means = [each_dec.get_text() for each_dec in each_property_mean.select('p span')]
        words_dict[word_property] = pep_word_means
    return {'yinbiao':words_alp, 'translation':words_dict, "sound": words_sound}

# def get_loacal_translation_from_iciba(word):
#     def get_yinbiao_fanyi(dicts, word):  ##获取音标和翻译
#
#         for dic in dicts:
#             dictItem = dic[1].get(word, 'no')
#             # print('dictItem=', dictItem)
#             if (dictItem != 'no'):
#                 return pharseDictItem(dic[0], dictItem)
###获取所有单词


if __name__ == "__main__":
    ''' words 的格式
    {
    book:{'freqs（总频率）':9, 'NNS':['books', 5(某个词性的频率),[sentences]]    },
    }
    '''
    with open('all_words.json', 'r', encoding='utf-8') as f:
        import json
        words_all=json.load(f)
    for word in words_all:
        for cixin in words_all[word]:
            if cixin=='freqs':
                continue
            tr=get_translation_from_iciba(words_all[word][cixin][0])
            words_all[word][cixin].insert(1, tr)

    #write to file
    with open('sdicts_from_iciba.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(words_all, f)
