uv=[]
for item in result:

    words=len(item[3]['high'])+len(item[3]['extra'])
    count = words/item[2]
    kk=item[-1]
    uv.append((kk[0], -kk[1], kk[2], count))




import json
def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

tt=[]
with open('高考/初中词_基础词.json', 'r', encoding='utf-8') as f:
    middle_words = json.load(f)
with open('高考/高中词汇2.json', 'r', encoding='utf-8') as f:
    high_words = json.load(f)
for word in middle_words:
    if syllable_count(word)>=3 and word in high_words:
        tt.append(word)
        print(word)