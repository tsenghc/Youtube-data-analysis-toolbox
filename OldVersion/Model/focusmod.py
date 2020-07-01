from OldVersion.Model.ytapi.channel_info import ChannelInfo
from OldVersion.Model.ytapi import VideoList
from OldVersion.Model.ytapi.videoInfo import VideoInfo
from OldVersion.Model.ytapi.comment import CommentThreadsSingle
from OldVersion.Model.integrate_list import Single
import json


class Focus():
    def __init__(self, datalist, FilterValue, DBsetting, SavePath):
        self.datalist = datalist
        self.FilterValue = FilterValue
        self.DBsetting = DBsetting
        self.SavePath = SavePath

    def getchannelinfo(self, channelID):
        Info = ChannelInfo(self.datalist, self.SavePath)
        try:
            self.datalist['id'] = channelID
            Info.squent_getInfo()
        except Exception as identifier:
            print(identifier)

    def getchannelplaylist(self, channelID):
        playlistid = ''
        filestate = Focus.checkfile(
            self, self.SavePath['channel_InfoPath'], channelID)
        if(filestate == 1):
            try:
                with open(self.SavePath['channel_InfoPath']+channelID+'.json', 'r') as f:
                    load_json = json.load(f)
                    playlistid = load_json[channelID]['relatedPlaylists']
                    VideoList.getchannelvideolist(self, playlistid, channelID)

            except Exception as identifier:
                print(identifier)
                pass
        else:
            print('無'+channelID+'資料集')
            Focus.getchannelinfo(self, channelID)
            print('取得'+channelID+'基本資訊中')
            Focus.getchannelplaylist(self, channelID)

    def getchannelvideoInfo(self, channelID):
        Single(self.datalist, self.SavePath)
        getvideoinfo = VideoInfo(self.datalist, self.SavePath)
        playlistid = ''
        try:
            with open(self.SavePath['channel_InfoPath']+channelID+'.json', 'r') as f:
                load_json = json.load(f)
                playlistid = load_json[channelID]['relatedPlaylists']

        except Exception as identifier:
            print(identifier)
            pass

        playlist = (Single.readchannelvideoPlayList(self, playlistid))
        VideoList = playlist[channelID]
        for id in VideoList:
            getvideoinfo.getchannelVideoInfo(id)

    def getchannelvideoTopcomment(self, channelID):
        self.datalist['exsistFile'] = self.SavePath['videocomment_ListPath']

        videoID = None
        Runcount = 0
        try:
            VideoList = Single.readchannelvideoPlayList(
                self, Single.channelID2playlistid(self, channelID=channelID))
            print(VideoList)
            if(VideoList != None):
                for videoID in VideoList[channelID]:
                    Runcount += 1
                    print('Total %.d statud %.2f' % (
                        len(VideoList[channelID]), (Runcount/len(VideoList[channelID])*100)))
                    CommentThreadsSingle.videoTopComment(
                        self, channelID, videoID)

            else:
                print('!videolist Error!')

        except Exception as identifier:
            print(identifier)
            pass

    def checkfile(self, path, filname):
        file = None
        try:
            with open(path+filname+'.json', 'r') as f:
                file = f
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('No such file') != -1:
                print('找不到'+path+filname+'檔案')

        if (file != None):
            return 1
        else:
            return 0
