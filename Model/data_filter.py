import os
import json

class DataFilter:
    def __init__(self,FilterValue,SavePath):
        self.FilterValue=FilterValue        
        self.SavePath=SavePath

    def channelFilter(self):
        Filelist=[]
        try:
            Filelist =(open(self.SavePath['channel_LogPath']+self.SavePath['ListFileName'],'r'))    
        except Exception as identifier:
            Error=str(identifier)            
            if Error.find('No such file')!=-1:
                print('找不到檔案')            
        filekey = []
        filevalue = []
        if ((Filelist)!= []):
                           
            with open(self.SavePath['channel_LogPath']+self.SavePath['InfoFileName'], 'r') as load_f:
                load_dict = json.load(load_f)
            for key,val in load_dict.items():
                if val['country']!="" and val['country'] in self.FilterValue['country']:
                    filekey.append(key)
                    filevalue.append(val)
            filekey = list(filekey)
            filevalue = list(filevalue)
            
            print('篩選後資料筆數'+str(len(filekey)))
        else:
            print("LOG目錄找不到頻道資訊")
        
        FilteredInfo=dict(zip(filekey,filevalue))
        DataFilter.WriteFile(self,FilteredInfo)
    
    def WriteFile(self,FilteredInfo):
            with open(self.SavePath['Filter_ListPath']+self.SavePath['FilteredData'], 'w') as f:
                json.dump(FilteredInfo, f)