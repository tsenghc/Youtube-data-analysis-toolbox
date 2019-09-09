from apiclient import discovery
import googleapiclient.discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import httplib2
import json
import time
import OAuth.APIOAuth

class ChannelInfo:

    def __init__(self, datalist,SavePath):
        self.data = datalist
        self.SavePath=SavePath
        self.data['part']='snippet,statistics,contentDetails' 

    #OLD API FUNCTION
    # Sample python code for channels.list
    # def remove_empty_kwargs(**kwargs):
    #     good_kwargs = {}
    #     if kwargs is not None:
    #         for key, value in kwargs.items():
    #             if value:
    #                 good_kwargs[key] = value
    #     return good_kwargs

    # def channels_list_by_id(client, **kwargs):
    #     # See full sample for function
    #     kwargs = ChannelInfo.remove_empty_kwargs(**kwargs)

    #     response = client.channels().list(
    #         **kwargs
    #     ).execute()

    #     return response
    # InfoList=ChannelInfo.channels_list_by_id(
    #                     self.data['service'],
    #                     part=self.data['part'],
    #                     id=self.data['id']
    #                     ) 

    def channel_info(self):
        api_service_name = "youtube"
        api_version = "v3"        
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        channelID=self.data['id']
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channelID
        ).execute()

        return request
    
    def squent_getInfo(self):
        InfoList=ChannelInfo.channel_info(self) 
        info=ChannelInfo.DecodeJson(self,InfoList)

        ChannelInfo.WriteFile(self,info)


    def DecodeJson(self,InfoList):
        channelid=""
        title=""
        description=""
        customurl=""
        publishedAt=""
        defaultLanguage=""
        country=""
        relatedplaylists=""
        viewcount=""
        subscribercount=""
        videocount=""  
        thumbnails=""           
        try:         
            channelid=(InfoList['items'][0]['id'])
        except Exception as identifier:
            print(identifier)
        try:
            title=(InfoList['items'][0]['snippet']['title'])
        except Exception as identifier:
            print(identifier)
        try:
            description=(InfoList['items'][0]['snippet']['description'])            
        except Exception as identifier:
            description=None
            print(identifier)
        try:
            publishedAt=(InfoList['items'][0]['snippet']['publishedAt'])      
        except Exception as identifier:
            print(identifier)
        try:
            relatedplaylists=(InfoList['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
        except Exception as identifier:
            print(identifier)
        try:
            viewcount=(InfoList['items'][0]['statistics']['viewCount'])
        except Exception as identifier:
            viewcount=None
            print(identifier)
        try:
            subscribercount=(InfoList['items'][0]['statistics']['subscriberCount'])
        except Exception as identifier:
            subscribercount=None
            print(identifier)
        try:
            videocount=(InfoList['items'][0]['statistics']['videoCount'])
        except Exception as identifier:
            videocount=None
            print(identifier)
        try:
            thumbnails=(InfoList['items'][0]['snippet']['thumbnails']['medium']['url'])
        except Exception as identifier:
            print(identifier)
        try:
            defaultLanguage=(InfoList['items'][0]['snippet']['defaultLanguage'])
        except Exception as identifier:
            defaultLanguage=None
            print(identifier)
        try:
            country=(InfoList['items'][0]['snippet']['country'])
        except Exception as identifier:
            print(identifier)
        try:
            customurl=(InfoList['items'][0]['snippet']['customUrl'])
        except Exception as identifier:
            print(identifier)        
        info={
            channelid:{                    
                'title':title,
                'description':description,
                'customurl':customurl,
                'publishedAt':publishedAt,
                'defaultLanguage':defaultLanguage,
                'country':country,
                'relatedPlaylists':relatedplaylists,
                'videoCount':videocount,
                'subscriberCount':subscribercount,
                'viewcount':viewcount,
                'thumbnails':thumbnails,
                'RequestDate':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            }
        }
        return info
        
    def WriteFile(self,info):
        with open(self.SavePath['channel_InfoPath']+self.data['id'] +'.json', 'w') as f:            
            json.dump(info, f)
            
            

# 使用channels 取得頻道資訊
#     * part=snippet,statistics,contentDetails,status
#     * Filters id=channelID(可串接統一查詢)
#     * 可取得內容
#         1. 頻道名稱title
#         2. 頻道描述description
#         3. 自訂連結customUrl
#         4. 頻道創建日期publishedAt
#         4. 頻道大頭貼thumbnails
#         5. 頻道預設語言defaultLanguage
#         6. 頻道國籍country
#         7. 所有影片清單contentDetails
#         8. 影片總觀看viewCount
#         9. 總訂閱人數subscriberCount
#         10. 是否公開訂閱人數hiddenSubscriberCount
#         11. 影片總數videoCount
#         12. 頻道公開狀態privacyStatus

