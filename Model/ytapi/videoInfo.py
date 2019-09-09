import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import OAuth.APIOAuth
import json
import time

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class VideoInfo():

    def __init__(self, datalist, SavePath):
        self.data = datalist
        self.SavePath = SavePath

    def video_info(self):

        api_service_name = "youtube"
        api_version = "v3"
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=self.data['id']
        ).execute()
        return request

    def getVideoInfo(self):

        videoInfo = VideoInfo.video_info(self)
        Info = VideoInfo.DecodeJson(self, videoInfo)
        VideoInfo.WriteFile(self, Info)

    def channelvideoinfo(self, videoid):

        api_service_name = "youtube"
        api_version = "v3"
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=videoid
        ).execute()
        return request

    def getchannelVideoInfo(self,videoid):
    
        videoInfo = VideoInfo.channelvideoinfo(self,videoid)
        self.data['id'] =videoid
        Info = VideoInfo.DecodeJson(self, videoInfo)        
        VideoInfo.WriteFile(self, Info)
        


    def DecodeJson(self, videoInfo):
        videoid = self.data['id']
        categoryId = ""
        channelId = ""
        channelTitle = ''
        videodescription = ''
        liveBroadcastContent = ''
        title = ''
        publishedAt = ''
        tags = []
        thumbnails = ''
        commentCount = 0
        dislikeCount = 0
        favoriteCount = 0
        likeCount = 0
        viewCount = 0

        try:
            categoryId = videoInfo['items'][0]['snippet']['categoryId']
        except Exception as identifier:
            print(identifier)
        try:
            channelId = videoInfo['items'][0]['snippet']['channelId']
        except Exception as identifier:
            print(identifier)
        try:
            channelTitle = videoInfo['items'][0]['snippet']['channelTitle']
        except Exception as identifier:
            print(identifier)
        try:
            videodescription = videoInfo['items'][0]['snippet']['description']
        except Exception as identifier:
            print(identifier)
        try:
            liveBroadcastContent = videoInfo['items'][0]['snippet']['liveBroadcastContent']
        except Exception as identifier:
            print(identifier)
        try:
            title = videoInfo['items'][0]['snippet']['localized']['title']
        except Exception as identifier:
            print(identifier)
        try:
            publishedAt = videoInfo['items'][0]['snippet']['publishedAt']
        except Exception as identifier:
            print(identifier)
        try:
            thumbnails = videoInfo['items'][0]['snippet']['thumbnails']['medium']['url']
        except Exception as identifier:
            print(identifier)
        try:
            viewCount = videoInfo['items'][0]['statistics']['viewCount']
        except Exception as identifier:
            print(identifier)
        try:
            likeCount = videoInfo['items'][0]['statistics']['likeCount']
        except Exception as identifier:
            print(identifier)
        try:
            dislikeCount = videoInfo['items'][0]['statistics']['dislikeCount']
        except Exception as identifier:
            print(identifier)
        try:
            favoriteCount = videoInfo['items'][0]['statistics']['favoriteCount']
        except Exception as identifier:
            print(identifier)
        try:
            tags = videoInfo['items'][0]['snippet']['tags']
        except Exception as identifier:
            print(identifier)
        try:
            commentCount = videoInfo['items'][0]['statistics']['commentCount']
        except Exception as identifier:
            print(identifier)

        Info = {
            videoid: {
                'categoryId': categoryId,
                'channelId': channelId,
                'channelName': channelTitle,
                'videodescription': videodescription,
                'liveBroadcastContent': liveBroadcastContent,
                'title': title,
                'publishedAt': publishedAt,
                'tags': tags,
                'thumbnails': thumbnails,
                'commentCount': commentCount,
                'dislikeCount': dislikeCount,
                'favoriteCount': favoriteCount,
                'likeCount': likeCount,
                'viewCount': viewCount,
                'RequestDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
        }
        return Info

    def WriteFile(self, get_Info):
        with open(self.SavePath['video_InfoPath']+self.data['id'] + '.json', 'w') as f:
            json.dump(get_Info, f)
            print('Write：'+self.data['id'])
