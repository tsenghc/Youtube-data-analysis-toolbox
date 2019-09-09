import json
from datetime import datetime, timedelta
import time
from Model.sql_function import SQLFunction
import os
from Model.integrate_list import Integrate

class Database:
    def __init__(self, datalist, DBsetting,SavePath):
        self.datalist = datalist
        self.DBsetting = DBsetting
        self.SavePath=SavePath

    def ChannelListPushDB(self):
        filekey = []
        filevalue = []
        with open(self.SavePath['channel_LogPath']+self.SavePath['ListFileName'], 'r') as load_f:
            load_dict = json.load(load_f)
        for keys in load_dict.keys():
            filekey.append(keys)
        for value in load_dict.values():
            filevalue.append(value)
        filekey = list((filekey))
        filevalue = list((filevalue))

        print('ReadDone \n 資料總比數:%d' % (len(filekey)))
        SQLFunction(self.DBsetting)
        Field = ['ChannelID', 'ChannelName']
        datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        Pstart = datetime.now()
        Tstart = datetime.now()
        for i in range(len(filekey)):
            Value = [filekey[i], filevalue[i]]
            try:
                SQLFunction.Inst('ChannelList', Field, Value)
            except Exception as identifier:
                print(identifier)

            Tend = datetime.now()
            if ((Tend-Tstart) > self.datalist['RefreshTime']):
                print('寫入資料庫進度: %.2f' % (i/len(filekey)*100))
                Tstart = datetime.now()
        Pend = datetime.now()
        print('寫入總耗時：%s  平均每秒比數：%s' %
              ((Pend-Pstart), len(filekey)/(Pend-Pstart)))

    def BatchChannelListInstDB(self):
        filekey = []
        filevalue = []
        with open(self.SavePath['channel_LogPath']+self.SavePath['ListFileName'], 'r') as load_f:
            load_dict = json.load(load_f)
        for keys in load_dict.keys():
            filekey.append(keys)
        for value in load_dict.values():
            filevalue.append(value)
        filekey = list((filekey))
        filevalue = list((filevalue))

        print('ReadDone \n 資料總比數:%d' % (len(filekey)))
        SQLFunction(self.DBsetting)
        Field = ['ChannelID', 'ChannelName']

        ChannelID = []
        ChannelName = []
        DiffID = []
        DiffName = []
        DBList = SQLFunction.raw_Search(self,'select ChannelID,ChannelName From ChannelList')
        for row in DBList:
            ChannelID.append(row[0])
            ChannelName.append(row[1])
        DiffID = list(set(filekey).difference(set(ChannelID)))
        DiffName = list(set(filevalue).difference(set(ChannelName)))
        print(DiffName)

        try:
            SQLFunction.BatchChannelInst('ChannelList', Field, DiffID, DiffName)
        except Exception as identifier:
            print(identifier)
            pass


    def BatchChannelInfoInstDB(self):
        filekey = []
        channelName = []
        channelDescript = []
        channelcusURL = []
        channelcreate = []
        channelcountry = []
        channelPlayList = []
        channelvideocount = []
        channelsubcount = []
        channelviewcount = []
        channelbanils = []
        channelRequestDate = []

        with open(self.SavePath['channel_LogPath']+self.SavePath['InfoFileName'], 'r') as load_f:
            load_dict = json.load(load_f)
        for keys in load_dict.keys():
            filekey.append(keys)
        for value in load_dict.values():
            channelName.append(value['title'])
            channelDescript.append(value['descript'])
            channelcusURL.append(value['customurl'])
            channelcreate.append(value['accountcreate'])
            channelcountry.append(value['country'])
            channelPlayList.append(value['relatedPlaylists'])
            channelvideocount.append(value['videocunt'])
            channelsubcount.append(value['subcount'])
            channelviewcount.append(value['viewcount'])
            channelbanils.append(value['thumbnails'])
            channelRequestDate.append(value['RequestDate'])

        Field = [
            'ChannelID',
            'ChannelName',
            'ChannelDescription',
            'ChannelCustomURL',
            'ChannelCreateDate',
            'ChannelCountry',
            'ChannelPlayList',
            'ChannelVideoCount',
            'ChannelSubCount',
            'ChannelViewCount',
            'ChannelBanils',
            'ChannelRequestDate'
        ]

        for i in range(len(filekey)):
            value = [
                filekey[i],
                channelName[i],
                channelDescript[i],
                channelcusURL[i],
                channelcreate[i][:20],
                channelcountry[i],
                channelPlayList[i],
                channelvideocount[i],
                channelsubcount[i],
                channelviewcount[i],
                channelbanils[i],
                channelRequestDate[i]
            ]
            try:
                SQLFunction(self.DBsetting)
                SQLFunction.BatchChannelInfoInst(self, 'ChannelInfo', Field, value)

            except Exception as identifier:
                print(identifier)
                pass

    def SquenVideoListInstDB(self):
        loadvideolist=Integrate.readchannelPlayList(self)
        filekey=[]        
        filevalue=[]
        for temp in loadvideolist:
            filekey.append(temp)
            for videoid in temp:
                filevalue.append(videoid)
        
        Field=[
            'ChannelID',
            'VideoID',            
        ]       

        db_videolist = SQLFunction.raw_Search(self,'select VideoID From ChannelVideoList')
        VideoID = []   
        for row in db_videolist:
            VideoID.append(row[0])
        diffvideoid = list(set(filevalue).difference(set(VideoID)))

        for channelid in loadvideolist:
            for videoid in loadvideolist[channelid]:
                if videoid not in diffvideoid:                
                    value=[
                        channelid,
                        videoid
                    ]   
                    
                    try:
                        SQLFunction(self.DBsetting)
                        SQLFunction.SquenVideoListInst(self, 'ChannelVideoList', Field,value )
                    except Exception as identifier:
                        print(identifier)
                        pass

    def BatchVideoListInstDB(self):
        loadvideolist=Integrate.readchannelPlayList(self)
        filekey=[]        
        filevalue=[]
        for temp in loadvideolist:
            filekey.append(temp)
            for videoid in loadvideolist[temp]:
                filevalue.append(videoid)
        
        Field=[
            'ChannelID',
            'VideoID',            
        ]       
        db_videolist = SQLFunction.raw_Search(self,'select VideoID From ChannelVideoList')
        VideoID = []   
        for row in db_videolist:
            VideoID.append(row[0])
        diffvideoid = list(set(filevalue).difference(set(VideoID)))
        print('jsonID'+str(len(filevalue)))
        print('db_exsistID'+str(len(db_videolist)))
        print(len(diffvideoid))
        channelid_list=[]
        videoid_list=[]

        ProcessStart = time.time()
        Tstart=time.time()
        RunCount=0
        BeforeRunCount=0

        for channelid in loadvideolist:
            for videoid in loadvideolist[channelid]:
                RunCount+=1
                if videoid in diffvideoid:  
                    channelid_list.append(channelid)             
                    videoid_list.append(videoid)
                else: 
                    pass
                
                # channelid_list.append(channelid)             
                # videoid_list.append(videoid)
                    
                Tend=time.time()
                if (Tend-Tstart)>=self.DBsetting['RefreshTime']:
                    print('status %.3f '%((RunCount/len(filevalue))*100))
                    print('Speed: %.d /s' % ((RunCount-BeforeRunCount)/self.DBsetting['RefreshTime']))
                    print('NeedTime:%.2f /min  already: %d s' % ((((len(filevalue)/(((RunCount-BeforeRunCount))/self.DBsetting['RefreshTime']))-((Tend-ProcessStart)))/60),(Tend-ProcessStart)))
                    print()
                    Tstart=time.time()
                    BeforeRunCount=RunCount

        value=[
            channelid_list,
            videoid_list
        ]   
        print(len(channelid_list))
        print(len(videoid_list))
        try:
            SQLFunction(self.DBsetting)
            SQLFunction.BatchVideoListInst(self, 'ChannelVideoList', Field,channelid_list,videoid_list )
        except Exception as identifier:
            print(identifier)
            pass


class FinalProjUsed:
    def __init__(self, datalist, DBsetting,SavePath):
        self.datalist = datalist
        self.DBsetting = DBsetting
        self.SavePath=SavePath

    def videoinfo_instdb(self,ChannelID):
        loadvideolist=Integrate.readchannelPlayList(self)
        filekey=[]        
        filevalue=[]
        for temp in loadvideolist:
            filekey.append(temp)
            for videoid in temp:
                filevalue.append(videoid)
        
        Field=[
            'SquenceHash',
            'ChannelID',
            'VideoID',
            'CategoryID',
            'VideoDescription',
            'liveBroadcastContent',
            'Titel',
            'PublishedAt',
            'tags',
            'Thumbnails',
            'RequestDate',
            'UpdateDate'

        ]       

        db_videolist = SQLFunction.raw_Search(self,'select VideoID From ChannelVideoList')
        VideoID = []   
        for row in db_videolist:
            VideoID.append(row[0])
        diffvideoid = list(set(filevalue).difference(set(VideoID)))

        for channelid in loadvideolist:
            for videoid in loadvideolist[channelid]:
                if videoid not in diffvideoid:                
                    value=[
                        channelid,
                        videoid
                    ]   
                    
                    try:
                        SQLFunction(self.DBsetting)
                        SQLFunction.SquenVideoListInst(self, 'ChannelVideoList', Field,value )
                    except Exception as identifier:
                        print(identifier)
                        pass
    
    pass
        

