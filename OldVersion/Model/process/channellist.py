from OldVersion.Model import SubscriptList
import time
import random
from OldVersion.main import Basic
from OldVersion.Model.integrate_list import Integrate


class getchannellist:

    def __init__(self, datalist,SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def getchannelList_test(self):
        getchannel = SubscriptList(datalist, SavePath)
        self.datalist['channelID'] = 'UC5h-QjcoM7g--01aa0F3n4A'
        getchannel.getSubscriptList()

    def getchannelList(self):
        self.datalist['exsistFile'] = self.SavePath['channel_ListPath']
        exisitList = Integrate.getsuccessList()
        getchannel = SubscriptList(self.datalist, self.SavePath)
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
                    self.datalist['channelID'] = key
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
            if ((Tend-Tstart) > self.datalist['RefreshTime']):
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