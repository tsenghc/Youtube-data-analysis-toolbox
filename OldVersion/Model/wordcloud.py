from wordcloud import WordCloud
from OldVersion.Model.jieba_split import Jiebatext


class Wordcloud():
    def __init__(self, datalist, SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def commentcloud(self, channelID):
        anaylsechar = Jiebatext.analysechannel(self, channelID)
        char = ""
        for i in anaylsechar:
            char += i+" "
        print(char)

        try:
            wc=WordCloud(
            width=3840, height=2160,
            font_path="NotoSansCJKtc-Black.otf",
            background_color="white",
            ).generate(char)

            wc.to_file(self.SavePath['wordcloudPIC_SavePath']+channelID+".jpg")
        except Exception as identifier:
            print(identifier)
