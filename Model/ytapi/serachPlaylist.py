import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import OAuth.APIOAuth
import json


class VideoList:
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    def __init__(self, datalist, SavePath):
        self.datalist = datalist
        self.SavePath = SavePath

    def playlistItems_list(self, nextPageToken):

        api_service_name = "youtube"
        api_version = "v3"
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        playlistid = self.datalist['playlistId']
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlistid,
            pageToken=nextPageToken
        ).execute()
        return request

    def getvideolist(self):

        ChannelVideoList = VideoList.playlistItems_list(self, nextPageToken='')

        NeedPage = int(ChannelVideoList['pageInfo']['totalResults'] /
                       ChannelVideoList['pageInfo']['resultsPerPage'])
        try:
            nextPageToken = ChannelVideoList['nextPageToken']
        except Exception as identifier:
            print(identifier)
            nextPageToken = ''
        i = 0
        videoid = []
        videopublish = []
        channelID = ''
        while (i <= NeedPage):

            videolist = VideoList.playlistItems_list(self, nextPageToken)
            channelID = videolist['items'][0]['snippet']['channelId']
            for j in range(0, len(videolist['items'])):
                videoid.append(videolist['items'][j]
                               ['contentDetails']['videoId'])
                videopublish.append(
                    videolist['items'][j]['contentDetails']['videoPublishedAt'])

            try:
                nextPageToken = videolist['nextPageToken']
            except Exception as identifier:
                print(identifier)
                nextPageToken = nextPageToken

            if NeedPage > 1:
                print('Download_Status:%.2f' % ((i/(NeedPage))*100))
            else:
                print('Download_Status:%.2f' % ((1/(1))*100))
            i += 1

            # if(videolist['pageInfo']['totalResults']%videolist['pageInfo']['resultsPerPage']==0):
            #     if(i<NeedPage):
            #         NeedPage=NeedPage-1
            #         nextPageToken = videolist['nextPageToken']
            #         i += 1
            #         #print('Download_Page:%.d' % i)
            #     else:
            #         i+=1
            #         #print('Download_Page:%.d' % i)
            #         #print('訂閱頻道數目與請求頁數之餘數為0無法取得下頁Token')
            # else:
            #     if (i <NeedPage):
            #         nextPageToken = videolist['nextPageToken']
            #         i += 1
            #         print('Download_Status:%.2f' % ((i/(NeedPage))*100))
            #     else:
            #         i += 1

        videolistJson = {
            channelID: videoid
        }

        VideoList.WriteFile(self, videolistJson)
        print(len(videoid))

    def channelplaylistItems(self, nextPageToken, playlistId):

        api_service_name = "youtube"
        api_version = "v3"
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        playlistid = playlistId
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=playlistid,
            pageToken=nextPageToken
        ).execute()
        return request

    def getchannelvideolist(self, playlistId, channelID):
        nextPageToken = ''
        page = 0
        videoid = []

        while(nextPageToken != None):
            ChannelVideoList = None
            resultsPerPage = 0
            try:
                ChannelVideoList = VideoList.channelplaylistItems(
                    self, nextPageToken=nextPageToken, playlistId=playlistId)
                resultsPerPage = ChannelVideoList['pageInfo']['resultsPerPage']
                nextPageToken = ChannelVideoList['nextPageToken']
                print(nextPageToken)
                page += 1
            except Exception as identifier:
                Error = str(identifier)
                if Error.find('nextPageToken', 0, 15) != -1:
                    nextPageToken = None
            print('PageCount:'+str(page))
            for i in range(len(ChannelVideoList['items'])):
                videoid.append(ChannelVideoList['items'][i]
                               ['contentDetails']['videoId'])

        videolistJson = {
            channelID: videoid
        }
        self.datalist['playlistId'] = playlistId
        VideoList.WriteFile(self, videolistJson)
        print(channelID+"-VideoCount-"+str(len(videoid)))

    def WriteFile(self, Subscriptdict):
        with open(self.SavePath['playlist_ListPath']+self.datalist['playlistId'] + '.json', 'w') as f:
            json.dump(Subscriptdict, f)
