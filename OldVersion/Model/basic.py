import os
import json
import requests
import threading
from OldVersion.Model.ytapi.subscriptionlist import SubscriptList
from OldVersion.Model.integrate_list import Integrate


class Basic():

    def __init__(self, datalist, SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def checkPath(self):
        if not os.path.isdir(SavePath['channel_ListPath']):
            os.mkdir(SavePath['channel_ListPath'])
        if not os.path.isdir(SavePath['channel_LogPath']):
            os.mkdir(SavePath['channel_LogPath'])
        if not os.path.isdir(SavePath['channel_InfoPath']):
            os.mkdir(SavePath['channel_InfoPath'])
        if not os.path.isdir(SavePath['Filter_ListPath']):
            os.mkdir(SavePath['Filter_ListPath'])
        if not os.path.isdir(SavePath['playlist_ListPath']):
            os.mkdir(SavePath['playlist_ListPath'])
        if not os.path.isdir(SavePath['videocomment_ListPath']):
            os.mkdir(SavePath['videocomment_ListPath'])
        if not os.path.isdir(SavePath['channelcomment_ListPath']):
            os.mkdir(SavePath['channelcomment_ListPath'])
        if not os.path.isdir(SavePath['wordcloudPIC_SavePath']):
            os.mkdir(SavePath['wordcloudPIC_SavePath'])
        if not os.path.isdir(SavePath['channel_VideoPath']):
            os.mkdir(SavePath['channel_VideoPath'])
        if not os.path.isdir(SavePath['video_InfoPath']):
            os.mkdir(SavePath['video_InfoPath'])
        print('Check Path Done')

    def firstRun(self):
        getchannel = SubscriptList(datalist, SavePath)
        try:
            getchannel.getSubscriptList()
        except Exception as identifier:
            Error = str(identifier)
            if Error.find('404', 0, 20) != -1:
                print('Error_404未找到位置(檢查網路問題)')
            elif Error.find('304', 0, 20) != -1:
                print('Error_304')
            elif Error.find('403', 0, 20) != -1:
                print('Error_403無法存取資料')
                pass

        Integrate.TotalchannelList()

    def deepRun(self):
        print('DeepRunStart')
        getchannel = SubscriptList(datalist, SavePath)
        datalist['exsistFile'] = SavePath['channel_ListPath']
        channelList = Integrate.readchannelList()
        exisitList = Integrate.getsuccessList()
        RunCount = 0
        for key in channelList:
            RunCount += 1
            print('DeepRun_Status: %.2f' % (RunCount/len(channelList)*100))
            try:
                if key not in exisitList:
                    datalist['channelID'] = key
                    getchannel.getSubscriptList()
                else:
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
                    # print(identifier)
                    pass

            else:
                pass
            finally:
                pass
        Integrate.TotalchannelList()
        print('DeepRunEnd')

    def getvideocategorie(self):
        rjson = ""
        categorie = []
        for i in range(50):
            try:
                r = requests.get("https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&hl=zh_TW&id="+str(
                    i)+"&key="+"")
                rjson = r.json()
                print(rjson['items'][0]['snippet']['title'])
                categorie.append(
                    rjson['items'][0]['snippet']['title']
                )
            except Exception as identifier:
                categorie.append("categoryUnknow")
                print(identifier)

        print(categorie)

        pass

    def runstatus(self, RunCount, RequestCount,
                  Tstart, Tend, RefreshCount,
                  ProcessStart, BeforeRunCount, listcount):
        print('Refresh Per %.d' % (RefreshCount))
        print('RefreshTime : %.2f /s' % (Tend-Tstart))
        print('Status: %.4f' % (RunCount/listcount*100))
        print('Request Count %.2f /s' % (RequestCount/(Tend-Tstart)))
        print('NeedTime:%.2f /min already: %d s' % ((((listcount /
                                                       (((RunCount-BeforeRunCount))/(Tend-Tstart))) -
                                                      ((Tend-ProcessStart)))/60), (Tend-ProcessStart)))
        print(threading.enumerate())
        print()




with open('./config/datalist.json', 'r') as datalist:
    datalist = json.loads(datalist.read())
with open('./config/SavePath.json', 'r') as path:
    SavePath = json.loads(path.read())

Integrate = Integrate(datalist, SavePath)
