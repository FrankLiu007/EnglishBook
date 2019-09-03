import json
from Clawer_tmp import lookup_word_all
import multiprocessing as mp
import threading as td
from multiprocessing import Process, Queue


with open("all_words.json", "rb") as f1:
    data = json.load(f1)
    # print(data)

word_dict = data.keys()
q1 = mp.Manager().Queue()


def job(q, word):
    res = lookup_word_all(word)
    while (res["sound"] == {}):
        res = lookup_word_all(word)
    q1.put(res)
    pass
po = mp.Pool(200)
word_dict = list(word_dict)
print(len(word_dict))
for word in word_dict[:1000]:
    print(word)
    po.apply_async(job, (q1,word, ))

po.close() # 关闭进程池
po.join() # 等待po中所有子进程执行完成

while not q1.empty():
    print(q1.get())