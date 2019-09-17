import requests
import re
import bs4



def lookup_word_all(word):
    words_dict = {}
    words_alp = {}
    words_sound = {}
    word_website = 'http://www.iciba.com/' + word
    res = requests.get(word_website, timeout=5)
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
    # print(word_alps)
    for alp in word_alps:
        print(alp)
        str_alp = str(alp.getText())
        alp_info = str_alp.split("[")
        if len(alp_info) > 1:
            words_alp[alp_info[0][:-1]] = "["+alp_info[1]
        else:
            words_alp["英"] = "["+alp_info[0]
    # print(words_alp)
    for each_property_mean in word_means:
        word_property = each_property_mean.select('span[class="prop"]')[0].get_text()
        pep_word_means = [each_dec.get_text() for each_dec in each_property_mean.select('p span')]
        words_dict[word_property] = pep_word_means
    return {"sound":words_sound,"alp":words_alp,"mean":words_dict,"word":word}


print(lookup_word_all("snow-covered"))
# lookup_word_all("sara")
