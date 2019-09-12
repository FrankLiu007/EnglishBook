import requests
import re
import bs4
import threading



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
    print(words_sound)
    for alp in word_alps:
        str_alp = str(alp.getText())
        alp_info = str_alp.split(" ")
        if len(alp_info)==1: ##只有1种发音的情况
            words_alp['all']=alp_info[0]
            break
        words_alp[alp_info[0]] = alp_info[1]

    print(words_alp)
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
###获取所有需要爬取翻译的单词
def get_words_need_translation(words_all):
    words_set=set()
    for word in words_all:
        for cixin in words_all[word]:
            if cixin=='freqs':
                continue
            words_set.add(words_all[word][cixin][0])

    return words_set

# ### 小项目，不用redis这些牛刀
# write words to redis
# def toRedis(words_set):
#     for word in words_set:
#         rconn.sadd("high:words",word)

def crawl_dict(words_set, words_dict, i):

    while words_set:
        word=words_set.pop()
        # print('word_set==null')
        try:
            print('get translations: ' + word )
            translation=get_translation_from_iciba(word)
            words_dict[word]=translation
        except:
            words_set.add(word)
    return 0

if __name__ == "__main__":
    ''' words 的格式
    {
    book:{'freqs（总频率）':9, 'NNS':['books', 5(某个词性的频率),[sentences]]    },
    }
    '''
    with open('all_words.json', 'r', encoding='utf-8') as f:
        import json
        words_all=json.load(f)

    words_set=get_words_need_translation(words_all)
    words_dict={}

    t_obj=[]
    for i in range(0,4):
        t=threading.Thread(target=crawl_dict, args=(words_set, words_dict, i))
        t.start()
        t_obj.append(t)

    for t in t_obj:
        t.join()
    print('crawler ends')


    #write to file
    with open('dicts_from_iciba.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(words_dict, f)



    #multiprocessing的方式
    # pool=multiprocessing.Pool(4)
    # pool.map(crawl_dict, range(4))
    # pool.close()
    # pool.join()

    # for word in words_all:
    #     for cixin in words_all[word]:
    #         if cixin=='freqs':
    #             continue
    #         dd=words_all[word][cixin][0]
    #         print("processing word: "+ dd)
    #         words_all[word][cixin].insert(1, words_dict[dd])

