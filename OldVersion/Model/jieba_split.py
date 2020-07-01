# encoding=utf-8
from OldVersion import jieba
import OldVersion.jieba.analyse
from OldVersion.Model.integrate_list import Integrate


class Jiebatext():
    def __init__(self, datalist, SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def cut_all(self, text):
        OldVersion.jieba.analyse.set_idf_path('./jieba/analyse/idfbig.txt')
        jieba.load_userdict('./jieba/dictbig.txt')
        jieba.set_dictionary('./jieba/dictbig.txt')
        #jieba.add_word(text,freq=None,tag=None)
        seg_list = jieba.cut(text, cut_all=True)
        seg_list = Jiebatext.stopword(self, seg_list)
        # print("Full Mode:",' '.join(seg_list))  # 全模式
        return (seg_list)

    def cut_foucus(self, text):
        OldVersion.jieba.analyse.set_idf_path('./jieba/analyse/idfbig.txt')
        jieba.load_userdict('./jieba/dictbig.txt')
        jieba.set_dictionary('./jieba/dictbig.txt')
        seg_list = jieba.cut(text, cut_all=False)
        seg_list = Jiebatext.stopword(self, seg_list)
        return seg_list
        # print("Default Mode:", "/ ".join(seg_list))  # 精确模式

    def cut_search(self, text):
        OldVersion.jieba.analyse.set_idf_path('./jieba/analyse/idfbig.txt')
        jieba.load_userdict('./jieba/dictbig.txt')
        jieba.set_dictionary('./jieba/dictbig.txt')
        seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
        seg_list = Jiebatext.stopword(self, seg_list)
        return seg_list
        #print(", ".join(seg_list))

    def analyse(self,text,topcount):
        OldVersion.jieba.analyse.set_idf_path('./jieba/analyse/idfbig.txt')
        jieba.load_userdict('./jieba/dictbig.txt')
        jieba.set_dictionary('./jieba/dictbig.txt')
        tag = (OldVersion.jieba.analyse.extract_tags(text,
                                                     topK=topcount, withWeight=True, allowPOS=()))
        
        return tag

    def analysechannel(self, channelID):
        OldVersion.jieba.analyse.set_idf_path('./jieba/analyse/idfbig.txt')
        jieba.load_userdict('./jieba/dictbig.txt')
        jieba.set_dictionary('./jieba/dictbig.txt')
        Integrate(self.datalist, self.SavePath)
        tag = (OldVersion.jieba.analyse.extract_tags(Integrate.readchannelcomment(self, channelID),
                                                     topK=200, withWeight=False, allowPOS=()))

        tag = Jiebatext.stopword(self, tag)
        return tag

        #print(jieba.analyse.textrank(Integrate.readchannelcomment(self), topK=100, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v','adj')))
    def stopword(self, segments):
        OldVersion.jieba.analyse.set_idf_path('./jieba/analyse/idfbig.txt')
        jieba.load_userdict('./jieba/dictbig.txt')
        jieba.set_dictionary('./jieba/dictbig.txt')
        with open('./jieba/stop_words.txt', "r") as word:
            stopwords = word.read()
        remainderWords = list(
            filter(lambda a: a not in stopwords and a != '\n', segments))

        return remainderWords
