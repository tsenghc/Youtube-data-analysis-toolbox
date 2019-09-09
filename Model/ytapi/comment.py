import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import OAuth.APIOAuth
import json
import time


class CommentThreads():

    def __init__(self, datalist, SavePath):
        self.data = datalist
        self.SavePath = SavePath

    def comment_threads(self, nextPageToken):

        api_service_name = "youtube"
        api_version = "v3"
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=self.data['id'],
            maxResults=100,
            pageToken=nextPageToken,
            order="time"
        ).execute()
        return request

    def channel_comment_threads(self, nextPageToken):
        api_service_name = "youtube"
        api_version = "v3"
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.commentThreads().list(
            part="snippet",
            allThreadsRelatedToChannelId=self.data['channelID'],
            maxResults=100,
            pageToken=nextPageToken,
            order="time",
            moderationStatus="published",
            textFormat="plainText"
        ).execute()
        return request

    def getcomment(self):
        commentid = []
        authorChannelId = []
        authorDisplayName = []
        likeCount = []
        publishedAt = []
        textOriginal = []
        updatedAt = []
        totalReplyCount = []
        nextPageToken = ''
        pagecount = 0
        while(nextPageToken != None):
            comment_top = None
            totalResults = 1
            try:
                comment_top = CommentThreads.comment_threads(
                    self, nextPageToken=nextPageToken)
                nextPageToken = comment_top['nextPageToken']
                totalResults = comment_top['pageInfo']['totalResults']
                pagecount += 1
            except Exception as identifier:
                Error = str(identifier)
                if Error.find('nextPageToken', 0, 15) != -1:
                    nextPageToken = None

            print('PageCount:'+str(pagecount))
            try:
                for i in range(totalResults):

                    commentid.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['id'])
                    authorChannelId.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
                    authorDisplayName.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                    likeCount.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'])
                    publishedAt.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'])
                    textOriginal.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
                    updatedAt.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['updatedAt'])
                    totalReplyCount.append(
                        comment_top['items'][i]['snippet']['totalReplyCount'])
            except Exception as identifier:
                print(identifier)
        pagecount = 0
        top_comment = []

        for j in range(len(commentid)):
            top_comment.append({
                self.data['id']: {
                    commentid[j]: {
                        'authorChannelId': authorChannelId[j],
                        'authorDisplayName': authorDisplayName[j],
                        'likeCount': likeCount[j],
                        'publishedAt': publishedAt[j],
                        'textOriginal': textOriginal[j],
                        'updatedAt': updatedAt[j],
                        'totalReplyCount': totalReplyCount[j]
                    }
                }

            })

        CommentThreads.WriteFile(self, top_comment)

    def channelTopComment(self):
        commentid = []
        authorChannelId = []
        authorDisplayName = []
        likeCount = []
        publishedAt = []
        textOriginal = []
        updatedAt = []
        totalReplyCount = []
        videoid = []
        nextPageToken = ''
        pagecount = 0
        while(nextPageToken != None):
            comment_top = None
            totalResults = 1
            try:
                comment_top = CommentThreads.channel_comment_threads(
                    self, nextPageToken=nextPageToken)
                nextPageToken = comment_top['nextPageToken']
                totalResults = comment_top['pageInfo']['totalResults']
                pagecount += 1
            except Exception as identifier:
                Error = str(identifier)
                if Error.find('nextPageToken', 0, 15) != -1:
                    nextPageToken = None

            print('PageCount:'+str(pagecount))
            try:
                for i in range(totalResults):
                    videoid.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['videoId'])
                    commentid.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['id'])
                    authorChannelId.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
                    authorDisplayName.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                    likeCount.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'])
                    publishedAt.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'])
                    textOriginal.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
                    updatedAt.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['updatedAt'])
                    totalReplyCount.append(
                        comment_top['items'][i]['snippet']['totalReplyCount'])
            except Exception as identifier:
                print(identifier)
        pagecount = 0
        top_comment = []

        for j in range(len(commentid)):
            try:
                top_comment.append({
                    self.data['channelID']: {
                        commentid[j]: {
                            'videoid': videoid[j],
                            'authorChannelId': authorChannelId[j],
                            'authorDisplayName': authorDisplayName[j],
                            'likeCount': likeCount[j],
                            'textOriginal': textOriginal[j],
                            'publishedAt': publishedAt[j],
                            'updatedAt': updatedAt[j],
                            'totalReplyCount': totalReplyCount[j]
                        }
                    }

                })
            except Exception as identifier:
                print(identifier)

        CommentThreads.WriteFile(self, top_comment)

    def WriteFile(self, top_comment):
        with open(self.SavePath['channelcomment_ListPath']+self.data['channelID'] + '.json', 'w') as f:
            json.dump(top_comment, f)


class CommentThreadsSingle:
    def __init__(self, datalist, SavePath):
        self.data = datalist
        self.SavePath = SavePath

    def comment_threads(self, nextPageToken, videoID):

        api_service_name = "youtube"
        api_version = "v3"
        credentials = OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=videoID,
            maxResults=100,
            pageToken=nextPageToken,
            order="time"
        ).execute()
        return request

    def videoTopComment(self, channelID, videoId):
        commentid = []
        authorChannelId = []
        authorDisplayName = []
        likeCount = []
        publishedAt = []
        textOriginal = []
        updatedAt = []
        totalReplyCount = []
        videoid = []
        nextPageToken = ''
        pagecount = 0
        while(nextPageToken != None):
            comment_top = None
            totalResults = 1
            try:
                comment_top = CommentThreadsSingle.comment_threads(
                    self, nextPageToken=nextPageToken, videoID=videoId)
                nextPageToken = comment_top['nextPageToken']
                totalResults = comment_top['pageInfo']['totalResults']
                pagecount += 1
            except Exception as identifier:
                Error = str(identifier)
                print(Error)
                if Error.find('nextPageToken', 0, 15) != -1:
                    nextPageToken = None
            print('PageCount:'+str(pagecount))
            try:

                for i in range(totalResults):
                    videoid.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['videoId'])
                    commentid.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['id'])
                    authorChannelId.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
                    authorDisplayName.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                    likeCount.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'])
                    publishedAt.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'])
                    textOriginal.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
                    updatedAt.append(
                        comment_top['items'][i]['snippet']['topLevelComment']['snippet']['updatedAt'])
                    totalReplyCount.append(
                        comment_top['items'][i]['snippet']['totalReplyCount'])
            except Exception as identifier:
                print(identifier)
        pagecount = 0
        top_comment = []

        for j in range(len(commentid)):
            try:
                top_comment.append({
                    channelID: {
                        commentid[j]: {
                            'videoid': videoid[j],
                            'authorChannelId': authorChannelId[j],
                            'authorDisplayName': authorDisplayName[j],
                            'likeCount': likeCount[j],
                            'textOriginal': textOriginal[j],
                            'publishedAt': publishedAt[j],
                            'updatedAt': updatedAt[j],
                            'totalReplyCount': totalReplyCount[j]
                        }
                    }

                })
            except Exception as identifier:
                print(identifier)

        CommentThreadsSingle.WriteFile(self, videoId, top_comment)

    def WriteFile(self, videoid, top_comment):
        with open(self.SavePath['videocomment_ListPath'] + videoid+'-commentTop' + '.json', 'w') as f:
            json.dump(top_comment, f)
