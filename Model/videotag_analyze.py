import os
import json
import random
import time
import nltk
from Model.jieba_split import Jiebatext
from Model.integrate_list import Integrate
from gensim import corpora, models, similarities


class TagAnalyze():
    def __init__(self, datalist, SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def jiebaweight(self, channelID):
        text = Integrate.readchannelVideotag_traget(self, channelID)

        cut = Jiebatext.cut_foucus(self, str(text))

        analyze = Jiebatext.analyse(self, str(cut), 10)

        print(analyze)
        return analyze

    def TFweight(self, channelID):
        keys = []
        values = []
        text = Integrate.readchannelVideotag_traget(self, channelID)
        wordcount = nltk.FreqDist(text)
        # print(wordcount.items())
        print('TagCount:%.d' % sum(wordcount.values()))
        for key in wordcount.keys():
            if ((wordcount[key]/sum(wordcount.values())) >= 0.01):
                keys.append(key)
                values.append(round(wordcount[key]/sum(wordcount.values()), 4))
        wordwidth = dict(zip(keys, values))
        # d3 = {k:v for k,v in wordwidth.items() if v > 0.01 }
        # print(list(d3))
        #wordwidth = list(filter(lambda x: wordwidth[x] >= 0.01, wordwidth))
        print(wordwidth)

        return wordwidth

    def TFIDF_cosinesimiliarity(self, text):
        pass

    def train(self, channelID):
        text = Integrate.readchannelVideotag_traget(self, channelID)
        cut = Jiebatext.cut_all(self, str(text))

        with open("./jieba/stop_words.txt") as f:
            stop_word_content = f.readlines()
        stop_word_content = [x.strip() for x in stop_word_content]
        stop_word_content = " ".join(stop_word_content)

        dictionary = corpora.Dictionary(document.split()
                                        for document in cut)

        stoplist = set(stop_word_content.split())
        stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
                    if stopword in dictionary.token2id]

        dictionary.compactify()
        texts = [[word for word in document.split() if word not in stoplist]
                 for document in cut]

        dictionary.save("./"+channelID+".dict")
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize("./"+channelID+".mm", corpus)

        # 載入語料庫
        if (os.path.exists("./"+channelID+".dict")):
            dictionary = corpora.Dictionary.load("./"+channelID+".dict")
            corpus = corpora.MmCorpus("./"+channelID+".mm")
            print("Used files generated from first tutorial")
        else:
            print("Please run first tutorial to generate data set")
        # 創建 tfidf model
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        # 創建 LSI model 潛在語義索引
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=99)
        corpus_lsi = lsi[corpus_tfidf]  # LSI潛在語義索引
        lsi.save("./"+channelID+".lsi")
        corpora.MmCorpus.serialize("./"+channelID+".mm", corpus_lsi)
        print("LSI topics:")
        lsi.print_topics(10)
        
        vec_bow = dictionary.doc2bow(cut) 
        # 用前面建好的 lsi 去計算這一篇歌詞
        vec_lsi = lsi[vec_bow] 
        #print(vec_lsi)

        # 建立索引
        #index = similarities.MatrixSimilarity(lsi[corpus]) 
        #index = similarities.MatrixSimilarity(tfidf[corpus_tfidf])
        index=similarities.Similarity("./"+channelID+".mm",corpus_tfidf,len(dictionary))
        index.save("./"+channelID+".index")
        # 相似度
        sims = index[vec_lsi] 
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        print(sims[:5])

        # 相似的前三首歌曲
        lyrics = [];
        fp = open(cut) # 斷詞後的歌詞
        for line in enumerate(fp):
            lyrics.append(line)
        fp.close()
        for lyric in sims[:3]:
            print("\n相似歌詞：",  lyrics[lyric[0]])
            print("相似度：",  lyric[1])


def edit_distance(self, w1, w2):
    l1, l2 = len(w1) + 1, len(w2) + 1
    matrix = [[0 for j in range(l2)] for i in range(l1)]
    for i in range(l1):
        matrix[i][0] = i
    for j in range(l2):
        matrix[0][j] = j
    for i in range(1, l1):
        for j in range(1, l2):
            delta = 0 if w1[i - 1] == w2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j - 1] + delta,
                               matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1)
    return matrix[-1][-1] / (l1 / 2 + l2 / 2 - 1)
