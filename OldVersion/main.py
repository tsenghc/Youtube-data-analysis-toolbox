# -*- coding: utf-8 -*-
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import getpass
import httplib2
import json
import random
import requests
import threading
from collections import Counter
from datetime import datetime, timedelta
import time
from OAuth.APIOAuth import get_credentials
from Model.ytapi.subscriptionlist import SubscriptList
from Model.ytapi.channel_info import ChannelInfo
from Model.ytapi.serachPlaylist import VideoList
from Model.ytapi.videoInfo import VideoInfo
from Model.ytapi.comment import CommentThreads, CommentThreadsSingle
from Model.data_filter import DataFilter
from Model.integrate_list import Integrate, Single
from Model.wordcloud import Wordcloud
from Model.jieba_split import Jiebatext
from Model.videotag_analyze import TagAnalyze
from Model.basic import Basic
from Model.focusmod import Focus
from Model.updateinfo import FileUpdate
import Model.database_control
import Model.sql_function
import difflib


class Process():

    def __init__(self, datalist, FilterValue, DBsetting, SavePath):
        self.datalist = datalist
        self.FilterValue = FilterValue
        self.DBsetting = DBsetting
        self.SavePath = SavePath

    def initialize_check(self):
        Basic.checkPath(SavePath)

    def simpleRun(self):
        Basic.firstRun(datalist)
        Basic.deepRun(datalist)
        print("simpleRun_Done")

    def getchannelList_test(self):
        getchannel = SubscriptList(datalist, SavePath)
        datalist['channelID'] = 'UC5h-QjcoM7g--01aa0F3n4A'
        getchannel.getSubscriptList()

    def getchannelList(self):
        datalist['exsistFile'] = SavePath['channel_ListPath']
        exisitList = Integrate.getsuccessList()
        getchannel = SubscriptList(datalist, SavePath)
        channelList = Integrate.readchannelList()
        random.shuffle(channelList)

        RunCount = 0
        RequestCount = 0
        RefreshCount = 0
        BeforeRunCount = 0
        listcount = len(channelList)

        Tstart = time.time()
        ProcessStart = time.time()
        for key in channelList:
            RunCount += 1
            try:
                if key not in exisitList:
                    datalist['channelID'] = key
                    getchannel.getSubscriptList()
                    RequestCount += 1
                else:
                    # print('IDexist')
                    pass
            except Exception as identifier:
                Error = str(identifier)
                if Error.find('404', 0, 20) != -1:
                    print('Error_404未找到位置(檢查網路問題)')
                elif Error.find('304', 0, 20) != -1:
                    print('Error_304')
                elif Error.find('403', 0, 20) != -1:
                    # print('Error_403無法存取資料')
                    pass
                else:
                    pass
                    # print(identifier)
            finally:
                pass

            Tend = time.time()
            if ((Tend-Tstart) > datalist['RefreshTime']):
                exisitList = Integrate.getsuccessList()
                Basic.runstatus(self, RunCount, RequestCount,
                                Tstart, Tend, RefreshCount,
                                ProcessStart, BeforeRunCount, listcount)
                RequestCount = 0
                RefreshCount = 0
                BeforeRunCount = RunCount
                Tstart = time.time()
            else:
                RefreshCount += 1
        ProcessEnd = time.time()
        print('GetChannel_List_Done')
        print('ProcessTimeCost : %.4f' % (ProcessEnd-ProcessStart))
        Integrate.TotalchannelList()

    def channelInfoTest(self):
        Info = ChannelInfo(datalist, SavePath)
        try:
            datalist['id'] = 'UCOFSGSKoIVb4Z2ZEAczUkvA'
            Info.squent_getInfo()

        except Exception as identifier:
            print(identifier)

    def getchannelInfo(self):
        Integrate.TotalchannelList()
        Info = ChannelInfo(datalist, SavePath)
        datalist['exsistFile'] = SavePath['channel_InfoPath']
        print('Count：' + str(len(Integrate.readchannelList())))
        RunCount = 0
        RequestCount = 0
        RefreshCount = 0
        BeforeRunCount = 0

        exisitList = Integrate.getsuccessList()
        channelList = Integrate.readchannelList()
        listcount = len(channelList)
        random.shuffle(channelList)
        ProcessStart = time.time()
        Tstart = time.time()

        for key in channelList:
            RunCount += 1
            if key not in exisitList:
                try:
                    datalist['id'] = key
                    Info.squent_getInfo()
                    RequestCount += 1
                except Exception as identifier:
                    print(identifier)
            else:
                # print('IDexist')
                pass

            Tend = time.time()

            if ((Tend-Tstart) > datalist['RefreshTime']):
                exisitList = Integrate.getsuccessList()
                Basic.runstatus(self, RunCount, RequestCount,
                                Tstart, Tend, RefreshCount,
                                ProcessStart, BeforeRunCount, listcount)
                RequestCount = 0
                RefreshCount = 0
                BeforeRunCount = RunCount
                Tstart = time.time()
            else:
                RefreshCount += 1

        Integrate.TotalchannelList()
        Integrate.TotalchannelInfo()
        ProcessEnd = time.time()
        print('GetChannel_Info_Done')
        print('ProcessTimeCost : %.4f /s' % (ProcessEnd-ProcessStart))

    def Filter(self):
        init_Filter = DataFilter(FilterValue, SavePath)
        init_Filter.channelFilter()

    def getFiltedVideolid(self):
        getvideolist = VideoList(datalist, SavePath)
        datalist['exsistFile'] = SavePath['playlist_ListPath']
        print('Count：' + str(len(Integrate.readFiltedPlayList())))
        RunCount = 0
        RequestCount = 0
        RefreshCount = 0
        BeforeRunCount = 0
        exisitList = Integrate.getsuccessList()
        FiltedPlayList = Integrate.readFiltedPlayList()
        listcount = len(FiltedPlayList)

        random.seed(datetime.utcnow())
        random.shuffle(FiltedPlayList)
        ProcessStart = time.time()
        Tstart = time.time()

        for key in FiltedPlayList:
            RunCount += 1
            if key not in exisitList:
                try:
                    datalist['playlistId'] = key
                    getvideolist.getvideolist()
                    RequestCount += 1
                except Exception as identifier:
                    Error = str(identifier)
                    if Error.find('404', 0, 20) != -1:
                        print('Error_404無法找到相關影片資訊')
                    elif Error.find('304', 0, 20) != -1:
                        print('Error_304')
                    elif Error.find('403', 0, 20) != -1:
                        # print('Error_403無法存取資料')
                        pass
                    else:
                        print(identifier)
            else:
                # print('IDexist')
                pass

            Tend = time.time()

            if ((Tend-Tstart) > datalist['RefreshTime']):
                exisitList = Integrate.getsuccessList()
                Basic.runstatus(self, RunCount, RequestCount,
                                Tstart, Tend, RefreshCount,
                                ProcessStart, BeforeRunCount, listcount)
                RequestCount = 0
                RefreshCount = 0
                BeforeRunCount = RunCount
                Tstart = time.time()
            else:
                RefreshCount += 1

        ProcessEnd = time.time()
        print('GetVideoList_Done')
        print('ProcessTimeCost : %.4f /s' % (ProcessEnd-ProcessStart))

    def getVideoInfo_test(self):
        getvideoinfo = VideoInfo(datalist, SavePath)
        datalist['id'] = '1Bl4lNWRseY'
        getvideoinfo.getVideoInfo()

    def getFiltedVideolInfo(self):
        getvideoinfo = VideoInfo(datalist, SavePath)
        datalist['id'] = Integrate.readchannelVideoID()
        datalist['exsistFile'] = SavePath['video_InfoPath']
        videolist = datalist['id']
        videolistID = []
        RunCount = 0
        BeforeRunCount = 0
        RequestCount = 0
        RefreshCount = 0
        exisitList = Integrate.getsuccessList()
        ProcessStart = time.time()
        Tstart = time.time()
        for temp in videolist:
            for videoid in temp:
                videolistID.append(videoid)
        listcount = len(videolistID)
        print('VideoCount:'+str(listcount))
        random.seed(datetime.utcnow())
        random.shuffle(videolistID)
        for videoid in videolistID:
            RunCount += 1
            if videoid not in exisitList:
                datalist['id'] = videoid
                getvideoinfo.getVideoInfo()
                RequestCount += 1
            else:
                pass
                # print('IDexsist')
            Tend = time.time()
            if ((Tend-Tstart) > datalist['RefreshTime']):
                exisitList = Integrate.getsuccessList()
                Basic.runstatus(self, RunCount, RequestCount,
                                Tstart, Tend, RefreshCount,
                                ProcessStart, BeforeRunCount, listcount)
                RequestCount = 0
                RefreshCount = 0
                BeforeRunCount = RunCount
                Tstart = time.time()
            else:
                RefreshCount += 1
        ProcessEnd = time.time()
        print('GetVideoInfo_Done')
        print('ProcessTimeCost : %.4f /s' % (ProcessEnd-ProcessStart))

    def getchannelVideoInfo_traget(self, channelID):
        Integrate.classifychannelVideoinfo_traget(channelID)

    def getFiltedCommentTop_test(self):
        getcomment = CommentThreads(datalist, SavePath)
        datalist['id'] = 'TOu5GnIyB_Y'
        getcomment.getcomment()

    def getFiltedCommentTop(self):
        getcomment = CommentThreads(datalist, SavePath)
        datalist['id'] = Integrate.readchannelVideoID()
        datalist['exsistFile'] = SavePath['channelcomment_ListPath']
        exisitList = Integrate.getsuccessList()
        filtedvideoid = Integrate.readchannelVideoID()

        random.seed(datetime.utcnow())
        random.shuffle(filtedvideoid)
        RunCount = 0
        BeforeRunCount = 0
        RequestCount = 0
        RefreshCount = 0

        videolistID = []
        ProcessStart = time.time()
        Tstart = time.time()
        for temp in filtedvideoid:
            for videoid in temp:
                videolistID.append(videoid)
        listcount = len(videolistID)
        print('VideoCount:'+str(listcount))

        for temp in videolistID:
            if temp not in exisitList:
                RunCount += 1
                datalist['id'] = temp
                getcomment.getcomment()
                RequestCount += 1
            else:
                pass
                # print('IDexsist')
            Tend = time.time()
            if ((Tend-Tstart) > datalist['RefreshTime']):
                exisitList = Integrate.getsuccessList()
                Basic.runstatus(self, RunCount, RequestCount,
                                Tstart, Tend, RefreshCount,
                                ProcessStart, BeforeRunCount, listcount)
                RequestCount = 0
                RefreshCount = 0
                BeforeRunCount = RunCount
                Tstart = time.time()
            else:
                RefreshCount += 1
        ProcessEnd = time.time()
        print('GetVideoComment_Done')
        print('ProcessTimeCost : %.4f /s' % (ProcessEnd-ProcessStart))

    def getchannelTopComment(self):
        getcomment = CommentThreads(datalist, SavePath)
        datalist['exsistFile'] = SavePath['channelcomment_ListPath']
        exisitList = Integrate.getsuccessList()
        channelID = Integrate.readFiltedchannelID()

        random.seed(datetime.utcnow())
        random.shuffle(channelID)

        RunCount = 0
        BeforeRunCount = 0
        RequestCount = 0
        RefreshCount = 0

        ProcessStart = time.time()
        Tstart = time.time()
        listcount = len(channelID)
        print('ChannelCount:'+str(listcount))

        for temp in channelID:
            if temp not in exisitList:
                RunCount += 1
                datalist['channelID'] = temp
                getcomment.channelTopComment()
                RequestCount += 1
            else:
                pass
                # print('IDexsist')
            Tend = time.time()
            if ((Tend-Tstart) > datalist['RefreshTime']):
                exisitList = Integrate.getsuccessList()
                Basic.runstatus(self, RunCount, RequestCount,
                                Tstart, Tend, RefreshCount,
                                ProcessStart, BeforeRunCount, listcount)
                RequestCount = 0
                RefreshCount = 0
                BeforeRunCount = RunCount
                Tstart = time.time()
            else:
                RefreshCount += 1
        ProcessEnd = time.time()
        print('GetVideoComment_Done')
        print('ProcessTimeCost : %.4f /s' % (ProcessEnd-ProcessStart))


try:
    with open('./config/SavePath.json', 'r') as path:
        SavePath = json.loads(path.read())
    with open('./config/datalist.json', 'r') as datalist:
        datalist = json.loads(datalist.read())
    with open('./config/FilterValue.json', 'r') as FilterValue:
        FilterValue = json.loads(FilterValue.read())
    with open('./config/DBsetting.json', 'r') as DBsetting:
        DBsetting = json.loads(DBsetting.read())
    with open('./config/category.json', 'r') as category:
        category = json.loads(category.read())
    print('config checked!')
except Exception as identifier:
    print(identifier)


Process = Process(datalist, FilterValue, DBsetting, SavePath)
Process.initialize_check()
Focusmod = Focus(datalist, FilterValue, DBsetting, SavePath)
FileUpdate = FileUpdate(datalist, FilterValue, DBsetting, SavePath)


Integrate = Integrate(datalist, SavePath)
Single = Single(datalist, SavePath)


# Integrate.TotalchannelList()
# Integrate.TotalchannelInfo()
# Integrate.TotalVideoList()
# Integrate.TotalvideoInfo()
# Integrate.readchannelInfo()
# Integrate.readFiltedPlayList()
# Integrate.readchannelList()
# Integrate.readchannelVideoID()
# Integrate.readchannelVideotag_traget("UCO3r3FllELijijdytnR43NA")

# comment_text=Integrate.readchannelcomment('UC24h-JBUHXT5HXIK_9cWOmQ')
# Jiebatext=Jiebatext(datalist,SavePath)
# comment_text=open('../jiebacut/'+'mycreate'+'.txt', 'r' ,encoding = 'utf8')

# jiebacut=Jiebatext.cut_all(comment_text.read())
# print(jiebacut)
# f=open('../jiebacut/'+'create'+'.txt', 'w',encoding='utf-8')
# f.write(str(' '.join(jiebacut)))
# f.write(comment_text)


# Wordcloud = Wordcloud(datalist, SavePath)
# Wordcloud.commentcloud('UCLW_SzI9txZvtOFTPDswxqg')

TagAnalyze = TagAnalyze(datalist, SavePath)
# Single.classifychannelVideoinfo_traget("UC24h-JBUHXT5HXIK_9cWOmQ")
# Single.classifychannelVideoinfo_traget("UCuLKTkYGCXako3wMktwrbkQ")
# t1 = TagAnalyze.TFweight("UC24h-JBUHXT5HXIK_9cWOmQ")
# t1 = str(list(t1)).replace('', '').replace('\'', '')
# t2 = TagAnalyze.TFweight("UCuLKTkYGCXako3wMktwrbkQ")
# t2 = str(list(t2)).replace('', '').replace('\'', '')
# j1 = TagAnalyze.jiebaweight("UC24h-JBUHXT5HXIK_9cWOmQ")
# j2 = TagAnalyze.jiebaweight("UCuLKTkYGCXako3wMktwrbkQ")
# TagAnalyze.train("UCuLKTkYGCXako3wMktwrbkQ")
# print(t1,t2)
# sm = difflib.SequenceMatcher(None, list(t1), list(t2))

# print(sm.ratio())

# Focusmod.getchannelinfo('UCuLKTkYGCXako3wMktwrbkQ')
# Focusmod.getchannelplaylist('UCuLKTkYGCXako3wMktwrbkQ')
#Focusmod.getchannelvideoInfo('UCuLKTkYGCXako3wMktwrbkQ')
FileUpdate.checkvideolist_update("UCuLKTkYGCXako3wMktwrbkQ")
Focusmod.getchannelvideoTopcomment('UCuLKTkYGCXako3wMktwrbkQ')

# m = tensorflow.keras.metrics.CosineSimilarity(axis=1)
# m.update_state([[0., 1.], [1., 1.]], [[1., 0.], [1., 1.]])
# print('Final result: ', m.result().numpy())  # Final result: 0.5


# Process.getchannelList_test(datalist)
# Process.channelInfoTest(datalist)
# Process.getVideoInfo_test(datalist)
# Process.getFiltedCommentTop_test()
# Process.getchannelTopComment()
# Process.getchannelVideoInfo_traget("UUKUlsqazP-4QmxdEtUPlxOA")
# Process.getchannelList(datalist)
# Process.getFiltedVideolInfo(datalist)#使用影片ID取得影片資訊


# Filter = DataFilter(FilterValue, SavePath)  # 過濾器
# Filter.channelFilter()

# Database=Model.database_control.Database(datalist,DBsetting,SavePath)
# Database.BatchChannelInfoInstDB()
# Database.BatchVideoListInstDB()


# Main.FirstRun(self=datalist)

# process.simpleRun(self=datalist)
# process.getchannelInfo(self=datalist)

# sql=Model.SQL_Function.SQLFunction(DBsetting)
# print(sql.raw_Search(SQL_text='SELECT ChannelList.ChannelName FROM ChannelList'))


# threads = []
# for i in range(4):
#     threads.append(threading.Thread(target =  process.getFiltedVideolid, args = (i,)))
#     threads[i].start()
#     print('getplaylist_start!'+str(i))
#     time.sleep(20)
# #process.getFiltedVideolid(self=datalist)#取得頻道撥放清單
# for i in range(4):
#     threads[i].join()
#     print('getplaylist_Done!'+str(i))
# Integrate.TotalVideoList(self=datalist)#統整影片ID


# threads = []
# for i in range(1):
#     threads.append(threading.Thread(target =  process.getFiltedVideolInfo, args = (i,)))
#     threads[i].start()
#     time.sleep(30)
#     print('getVideoInfo_start!'+str(i))

# #process.getFiltedVideolInfo(self=datalist)#使用影片ID取得影片資訊
# for i in range(1):
#     threads[i].join()
#     print('getVideoInfo_Done!'+str(i))
# Integrate.TotalvideoInfo(self=datalist)#統整影片資訊


# threads = []
# for i in range(2):
#     threads.append(threading.Thread(target =  Process.getchannelTopComment, args = (i,)))
#     threads[i].start()
#     time.sleep(30)
#     print('getVideoInfo_start!'+str(i))

# for i in range(2):
#     threads[i].join()
#     print('getVideoInfo_Done!'+str(i))
