import os
import json
import time


class Integrate:
    def __init__(self, datalist, SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def TotalchannelList(self):
        Filelist = []
        for root, dirs, files in os.walk(self.SavePath['channel_ListPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))
        filekey = []
        filevalue = []
        if (len(Filelist) > 0):
            for i in range(len(Filelist)):
                filedir = Filelist[i]
                with open(filedir, 'r') as load_f:
                    load_dict = json.load(load_f)
                # if load_dict.keys() not in filekey:
                    for keys in load_dict.keys():
                        filekey.append(keys)
                    for value in load_dict.values():
                        filevalue.append(value)
            filekey = list((filekey))
            filevalue = list((filevalue))
            #####
            # 查看重複內容
            # a=set()
            # b=[]
            # for x in filekey:
            #     if x not in a:
            #         a.add(x)
            #     else:
            #         b.append(x)
            # print(len(b))
            #####
            with open(self.SavePath['channel_LogPath']+self.SavePath['ListFileName'], 'w') as f:
                channelList = dict(zip(filekey, filevalue))
                json.dump(channelList, f)
            print('載入總頻道數'+str(len(set(filekey))))
        else:
            print("channelList查無存取目錄或目錄內無檔案")

    def TotalchannelInfo(self):
        Filelist = []
        for root, dirs, files in os.walk(self.SavePath['channel_InfoPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))
        filekey = []
        filevalue = []
        if (len(Filelist) > 0):
            for i in range(len(Filelist)):
                filedir = Filelist[i]
                with open(filedir, 'r') as load_f:
                    load_dict = json.load(load_f)
                for keys in load_dict.keys():
                    filekey.append(keys)
                for value in load_dict.values():
                    filevalue.append(value)
            filekey = list(filekey)
            filevalue = list(filevalue)

            with open(self.SavePath['channel_InfoPath']+self.SavePath['InfoFileName'], 'w') as f:
                channelList = dict(zip(filekey, filevalue))
                json.dump(channelList, f)
            print('頻道資訊比數'+str(len(filekey)))
        else:
            print("channelINFO查無存取目錄或目錄內無檔案")

    def readchannelList(self):
        Filelist = []
        try:
            Filelist = (
                open(self.SavePath['channel_LogPath']+self.SavePath['ListFileName'], 'r'))
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('No such file') != -1:
                print('找不到檔案')
        filekey = []
        filevalue = []

        if ((Filelist) != []):
            with open(self.SavePath['channel_LogPath']+self.SavePath['ListFileName'], 'r') as load_f:
                load_dict = json.load(load_f)
            for keys in load_dict.keys():
                filekey.append(keys)
            for value in load_dict.values():
                filevalue.append(value)
            filekey = list(set(filekey))
            filevalue = list(set(filevalue))

            # print('載入總頻道數'+str(len(filevalue)))
        else:
            print("Log目錄或目錄內無檔案")
        return filekey

    def readchannelInfo(self):
        Filelist = []
        try:
            Filelist = (
                open(self.SavePath['channel_LogPath']+self.SavePath['InfoFileName'], 'r'))
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('No such file') != -1:
                print('找不到檔案')
        filekey = []
        filevalue = []
        if ((Filelist) != []):

            with open(self.SavePath['channel_LogPath']+self.SavePath['InfoFileName'], 'r') as load_f:
                load_dict = json.load(load_f)
            for keys in load_dict.keys():
                filekey.append(keys)
            for value in load_dict.values():
                filevalue.append(value)
            filekey = list(filekey)
            filevalue = list(filevalue)

            print('頻道資訊比數'+str(len(filekey)))
        else:
            print("Log目錄或目錄內無檔案")
        return "Done"

    def channelList_traget(self):
        Filelist = []
        for root, dirs, files in os.walk(self.SavePath['channel_ListPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))
        filekey = []
        filevalue = []
        if (len(Filelist) > 0):
            filedir = self.SavePath['channel_ListPath'] + \
                self.SavePath['channelID']+'.json'
            with open(filedir, 'r') as load_f:
                load_dict = json.load(load_f)
                for keys in load_dict.keys():
                    filekey.append(keys)
                for value in load_dict.values():
                    filevalue.append(value)
            filekey = list(set(filekey))
            filevalue = list(set(filevalue))
        else:
            print("channelList目錄或目錄內無檔案")
        return filekey

    def getsuccessList(self):
        Filelist = []
        for root, dirs, files in os.walk(self.datalist['exsistFile']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.splitext(file)[0])

        return Filelist

    def readFiltedPlayList(self):
        Filelist = []
        for root, dirs, files in os.walk(self.SavePath['Filter_ListPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))
        filekey = []
        filevalue = []
        if (len(Filelist) > 0):
            filedir = self.SavePath['Filter_ListPath'] + \
                self.SavePath['FilteredData']
            with open(filedir, 'r') as load_f:
                load_dict = json.load(load_f)
                for keys in load_dict.keys():
                    filekey.append(keys)
                for value in load_dict.values():
                    filevalue.append(value['relatedPlaylists'])
            filekey = list((filekey))
            filevalue = list((filevalue))
        else:
            print("Filter_ListPath目錄或目錄內無檔案")
        return filevalue

    def readFiltedchannelID(self):
        Filelist = []
        for root, dirs, files in os.walk(self.SavePath['Filter_ListPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))
        filekey = []
        filevalue = []
        if (len(Filelist) > 0):
            filedir = self.SavePath['Filter_ListPath'] + \
                self.SavePath['FilteredData']
            with open(filedir, 'r') as load_f:
                load_dict = json.load(load_f)
                for keys in load_dict.keys():
                    filekey.append(keys)

            filekey = list((filekey))

        else:
            print("Filter_ListPath目錄或目錄內無檔案")
        return filekey

    def TotalVideoList(self):
        Tstart = time.time()

        Filelist = []
        for root, dirs, files in os.walk(self.SavePath['playlist_ListPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))
        filekey = []
        filevalue = []

        Tend = time.time()
        print('LoadingVideoList time consuming: %.2f s' % (Tend-Tstart))

        Tstart = time.time()
        if (len(Filelist) > 0):
            for i in range(len(Filelist)):
                filedir = Filelist[i]
                try:
                    with open(filedir, 'r') as load_f:
                        load_dict = json.load(load_f)
                    for keys in load_dict.keys():
                        filekey.append(keys)
                    for value in load_dict.values():
                        filevalue.append(value)
                except Exception as identifier:
                    os.remove(filedir)
                    print(filedir)
                    print(identifier)

            filekey = list(filekey)
            filevalue = list(filevalue)

            Tend = time.time()
            print('CombineList time consuming: %.2f s' % (Tend-Tstart))

            with open(self.SavePath['playlist_LogPath']+self.SavePath['PlayListFileName'], 'w') as f:
                channelList = dict(zip(filekey, filevalue))
                json.dump(channelList, f)
            print('頻道資訊比數'+str(len(filekey)))
        else:
            print("palylist查無存取目錄或目錄內無檔案")

    def TotalvideoInfo(self):
        Tstart = time.time()

        Filelist = []
        for root, dirs, files in os.walk(self.SavePath['video_InfoPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))

        Tend = time.time()
        print('LoadingVideoInfo time consuming: %.2f s' % (Tend-Tstart))

        filekey = []
        filevalue = []
        Tstart = time.time()

        if (len(Filelist) > 0):
            for i in range(len(Filelist)):
                filedir = Filelist[i]
                try:
                    with open(filedir, 'r') as load_f:
                        load_dict = json.load(load_f)
                    for keys in load_dict.keys():
                        filekey.append(keys)
                    for value in load_dict.values():
                        filevalue.append(value)
                except Exception as identifier:
                    os.remove(filedir)
                    print(filedir)
                    print(identifier)
            filekey = list(filekey)
            filevalue = list(filevalue)

            Tend = time.time()
            print('CombineInfo time consuming: %.2f s' % (Tend-Tstart))

            with open(self.SavePath['videoInfo_LogPath']+self.SavePath['videoInfoName'], 'w') as f:
                channelList = dict(zip(filekey, filevalue))
                json.dump(channelList, f)
            print('頻道資訊比數'+str(len(filekey)))
        else:
            print("videoInfo查無存取目錄或目錄內無檔案")

    def readchannelVideoID(self):
        Filelist = []
        try:
            Filelist = (
                open(self.SavePath['playlist_LogPath']+self.SavePath['PlayListFileName'], 'r'))
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('No such file') != -1:
                print('找不到videolist檔案')
        filekey = []
        filevalue = []
        if ((Filelist) != []):

            with open(self.SavePath['playlist_LogPath']+self.SavePath['PlayListFileName'], 'r') as load_f:
                load_dict = json.load(load_f)
            for keys in load_dict.keys():
                filekey.append(keys)
            for value in load_dict.values():
                filevalue.append((value))
            filekey = list(filekey)
            filevalue = list(filevalue)

            print('影片筆數'+str(len(filekey)))

        else:
            print("Log目錄或目錄內無檔案")
        return filevalue

    def readchannelPlayList(self):
        Filelist = []
        try:
            Filelist = (
                open(self.SavePath['playlist_LogPath']+self.SavePath['PlayListFileName'], 'r'))
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('No such file') != -1:
                print('找不到PlayList檔案')

        if ((Filelist) != []):

            with open(self.SavePath['playlist_LogPath']+self.SavePath['PlayListFileName'], 'r') as load_f:
                load_dict = json.load(load_f)

            print('頻道筆數'+str(len(load_dict)))

        else:
            print("Log目錄或目錄內無檔案")
        return load_dict

    def readchannelcomment(self, channelID):
        Filelist = []
        comment = ""
        try:
            Filelist = (
                open(self.SavePath['videocomment_ListPath']+channelID+".json", 'r'))
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('No such file') != -1:
                print('找不到comment檔案')
        if ((Filelist) != []):
            with open(self.SavePath['videocomment_ListPath']+channelID+".json", 'r') as load_f:
                load_dict = json.load(load_f)
            for i in range(len(load_dict)):
                for keys in load_dict[i].keys():
                    for deepkeys in load_dict[i][keys].keys():
                        comment += (load_dict[i][keys]
                                    [deepkeys]['textOriginal'])
        else:
            print("Log目錄或目錄內無檔案")

        return comment

    def classifychannelVideoinfo(self):
        Filelist = []
        filekey = []
        filevalue = []
        fail = 0
        sucess = 0
        for root, dirs, files in os.walk(self.SavePath['playlist_ListPath']):
            for file in files:
                if os.path.splitext(file)[1] == '.json':
                    Filelist.append(os.path.join(root, file))
        if ((Filelist) != []):
            for channel in Filelist:
                try:
                    with open(channel, 'r') as load_f:
                        load_dict = json.load(load_f)
                        for keys in load_dict.keys():
                            filekey.append(keys)
                        for values in load_dict.values():
                            for video in values:
                                try:
                                    with open(self.SavePath['video_InfoPath']+str(video)+'.json', 'r') as videoinfo:
                                        # print(json.load(videoinfo))
                                        filevalue.append(json.load(videoinfo))
                                        sucess += 1

                                except Exception as identifier:
                                    # print(identifier)
                                    fail += 1
                                    pass

                    channelvideo = {
                        keys: filevalue
                    }
                    # print(channelvideo)

                    with open(self.SavePath['channel_VideoPath']+keys+'.json', 'w') as f:
                        print('fail %.d success %.d' % (fail, sucess))
                        json.dump(channelvideo, f)
                        filekey = []
                        filevalue = []
                        fail = 0
                        sucess = 0
                except Exception as identifier:
                    print(identifier)
                    pass

    def classifychannelVideoinfo_traget(self, playlistid):
        filekey = []
        filevalue = []
        fail = 0
        sucess = 0
        try:
            with open(self.SavePath['playlist_ListPath']+playlistid+'.json', 'r') as load_f:
                load_dict = json.load(load_f)
                for keys in load_dict.keys():
                    filekey.append(keys)
                for values in load_dict.values():
                    for video in values:
                        try:
                            with open(self.SavePath['video_InfoPath']+str(video)+'.json', 'r') as videoinfo:
                                # print(json.load(videoinfo))
                                filevalue.append(json.load(videoinfo))
                                sucess += 1

                        except Exception as identifier:
                            # print(identifier)
                            fail += 1
                            pass

            channelvideo = {
                keys: filevalue
            }
            # print(channelvideo)

            with open(self.SavePath['channel_VideoPath']+keys+'.json', 'w') as f:
                print('fail %.d success %.d' % (fail, sucess))
                json.dump(channelvideo, f)
                filekey = []
                filevalue = []
                fail = 0
                sucess = 0
        except Exception as identifier:
            print(identifier)
            pass

    def readchannelVideotag_traget(self, channelID):
        videotag = []
        try:
            with open(self.SavePath['channel_VideoPath']+channelID+'.json', 'r') as f:
                load_dict = json.load(f)
                print('VideoCount:%.d' % len(load_dict[channelID]))
                for i in range(len(load_dict[channelID])):
                    for key in load_dict[channelID][i].keys():
                        for tag in load_dict[channelID][i][key]['tags']:
                            videotag.append(tag)

        except Exception as identifier:
            print(identifier)

        return videotag


class Single():
    def __init__(self, datalist, SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def channelID2playlistid(self, channelID):
        try:
            with open(self.SavePath['channel_InfoPath']+channelID+'.json', 'r') as f:
                load_json = json.load(f)
                playlistid = load_json[channelID]['relatedPlaylists']
                return playlistid
        except Exception as identifier:
            print(identifier)
            pass

    def readchannelvideoPlayList(self, playlistid):
        Filelist = []
        try:
            Filelist = (
                open(self.SavePath['playlist_ListPath']+playlistid+'.json', 'r'))
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('No such file') != -1:
                print('找不到PlayList檔案')

        if ((Filelist) != []):

            with open(self.SavePath['playlist_ListPath']+playlistid+'.json', 'r') as load_f:
                load_dict = json.load(load_f)
            return load_dict
        else:
            print("Log目錄或目錄內無檔案")

    def classifychannelVideoinfo_traget(self, channelID):
        filekey = []
        filevalue = []
        items = []
        fail = 0
        sucess = 0
        playlistid = Single.channelID2playlistid(self, channelID)
        try:
            with open(self.SavePath['playlist_ListPath']+playlistid+'.json', 'r') as load_f:
                load_dict = json.load(load_f)
                for keys in load_dict.keys():
                    filekey.append(keys)
                for values in load_dict.values():
                    for video in values:
                        try:
                            with open(self.SavePath['video_InfoPath']+str(video)+'.json', 'r') as videoinfo:
                                # print(json.load(videoinfo))
                                filevalue.append(json.load(videoinfo))

                                sucess += 1

                        except Exception as identifier:
                            # print(identifier)
                            fail += 1
                            pass

            channelvideo = {
                keys: filevalue
            }
            # print(channelvideo)
            print(items)
            with open(self.SavePath['channel_VideoPath']+keys+'.json', 'w') as f:
                print('fail %.d success %.d' % (fail, sucess))
                json.dump(channelvideo, f)
                filekey = []
                filevalue = []
                fail = 0
                sucess = 0
        except Exception as identifier:
            print(identifier)
            pass
