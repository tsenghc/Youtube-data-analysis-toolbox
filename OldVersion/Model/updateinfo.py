import os
import time
from OldVersion.Model.integrate_list import Single
from OldVersion.Model.focusmod import Focus


class FileUpdate():
    def __init__(self, datalist, FilterValue, DBsetting, SavePath):
        self.datalist = datalist
        self.FilterValue = FilterValue
        self.DBsetting = DBsetting
        self.SavePath = SavePath

    def checkvideolist_update(self, channelID):
        exisittime = FileUpdate.getchannelvideolist_existtime(self, channelID)
        if(int(exisittime) >= 60):
            print('exisit-time: %.d hours, %.s Need update' %
                  (int(exisittime/60), str(channelID)))
            FileUpdate.updatechannelvideoinfo(self, channelID)
        else:
            print(channelID+"-don't need update")

    def getchannelvideolist_existtime(self, channelID):

        CreateTime = time.localtime(os.stat(
            self.SavePath['channel_VideoPath']+channelID+'.json').st_mtime)  # 文件访问时间
        Createyear = int(time.strftime('%Y', CreateTime))
        Createmon = int(time.strftime('%m', CreateTime))
        Createday = int(time.strftime('%d', CreateTime))
        CreateHours = int(time.strftime('%H', CreateTime))
        CreateMin = int(time.strftime('%M', CreateTime))

        NowTime = time.localtime()
        Nowyear = int(time.strftime('%Y', NowTime))
        Nowmon = int(time.strftime('%m', NowTime))
        Nowday = int(time.strftime('%d', NowTime))
        NowHours = int(time.strftime('%H', NowTime))
        NowMin = int(time.strftime('%M', NowTime))

        diffYear = Nowyear-Createyear
        diffmon = Nowmon-Createmon
        diffday = Nowday-Createday
        diffhour = NowHours-CreateHours
        diffmin = NowMin-CreateMin
        print(diffYear, diffmon, diffday, diffhour, diffmin)
        difftime = abs(diffday*24*60+diffhour*60+diffmin)
        # print(difftime)
        return difftime

    def checkfile_existtime(self,Path):
        CreateTime = time.localtime(os.stat(Path).st_mtime)  # 文件访问时间
        Createyear = int(time.strftime('%Y', CreateTime))
        Createmon = int(time.strftime('%m', CreateTime))
        Createday = int(time.strftime('%d', CreateTime))
        CreateHours = int(time.strftime('%H', CreateTime))
        CreateMin = int(time.strftime('%M', CreateTime))

        NowTime = time.localtime()
        Nowyear = int(time.strftime('%Y', NowTime))
        Nowmon = int(time.strftime('%m', NowTime))
        Nowday = int(time.strftime('%d', NowTime))
        NowHours = int(time.strftime('%H', NowTime))
        NowMin = int(time.strftime('%M', NowTime))

        diffYear = Nowyear-Createyear
        diffmon = Nowmon-Createmon
        diffday = Nowday-Createday
        diffhour = NowHours-CreateHours
        diffmin = NowMin-CreateMin
        print('Y:%.d M:%.d D:%.d H:%.d m:%.d' %(diffYear, diffmon, diffday, diffhour, diffmin))
        difftime = abs(diffday*24*60+diffhour*60+diffmin)
        # print(difftime)
        return difftime
        

    def updatechannelvideoinfo(self, channelID):
        print('update %.s' % str(channelID))

        Focusmod = Focus(self.datalist, self.FilterValue,
                         self.DBsetting, self.SavePath)
        Focusmod.getchannelplaylist(channelID)
        Focusmod.getchannelvideoInfo(channelID)
        Single.classifychannelVideoinfo_traget(self, channelID)
        pass
