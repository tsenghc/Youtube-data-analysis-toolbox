# -*- coding: utf-8 -*- 
import googleapiclient.discovery
import json
import OldVersion.OAuth.APIOAuth


class SubscriptList():   

    def __init__(self, datalist,SavePath):
        self.data = datalist
        self.SavePath=SavePath
        
   
    # def remove_empty_kwargs(**kwargs):
    #     good_kwargs = {}
    #     if kwargs is not None:
    #         for key, value in kwargs.items():
    #             if value:
    #                 good_kwargs[key] = value
    #     return good_kwargs


    # def subscriptions_list_by_channel_id(client, **kwargs):
    #     # See full sample for function
    #     kwargs = SubscriptList.remove_empty_kwargs(**kwargs)    
    #     response = client.subscriptions().list(
    #         **kwargs
    #     ).execute()
    #     return response
    

    def subscriptions_list_by_channelid(self,nextPageToken):
        api_service_name = "youtube"
        api_version = "v3"
        credentials = OldVersion.OAuth.APIOAuth.get_credentials()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials = credentials)

        request = youtube.subscriptions().list(
            part="snippet",
            channelId=self.data['channelID'],
            maxResults='50',
            pageToken=nextPageToken
        ).execute()

        return request

    
    def getSubscriptList(self):       
        channelID_List=[]
        channelName_List=[]        
        sublist=SubscriptList.subscriptions_list_by_channelid(self,nextPageToken='')
        NeedPage=int(sublist['pageInfo']['totalResults']/sublist['pageInfo']['resultsPerPage'])
        try:
            nextPageToken=sublist['nextPageToken']
        except Exception as identifier:
                print(identifier)
                nextPageToken=''
        print(sublist['pageInfo']['totalResults'])
        i=0
        
        while (i<=NeedPage):
            
            sublist=SubscriptList.subscriptions_list_by_channelid(self,nextPageToken=nextPageToken)
            
            for j in range(0,len(sublist['items'])):    
                channelName_List.append(sublist['items'][j]['snippet']['title']) 
                channelID_List.append(sublist['items'][j]['snippet']['resourceId']['channelId'])
            
            try:
                nextPageToken = sublist['nextPageToken']
            except Exception as identifier:
                print(identifier)
                nextPageToken=nextPageToken

            if NeedPage>1:
                print('Download_Status:%.2f' % ((i/(NeedPage))*100)) 
            else:
                print('Download_Status:%.2f' % ((1/(1))*100)) 
            i += 1

            # if(sublist['pageInfo']['totalResults']%sublist['pageInfo']['resultsPerPage']==0):
            #     if(i<NeedPage):
            #         NeedPage=NeedPage-1
            #         nextPageToken = sublist['nextPageToken']       
            #         i += 1
            #         #print('Download_Page:%.d' % i)
            #     else:      
            #         i+=1
            #         #print('Download_Page:%.d' % i)                    
            #         #print('訂閱頻道數目與請求頁數之餘數為0無法取得下頁Token')
            # else:
            #     if (i <NeedPage):                    
            #         nextPageToken = sublist['nextPageToken']
            #         i += 1
            #         print('Download_Status:%.2f' % ((i/(NeedPage))*100))                                       
            #     else:
            #         i += 1
        print('訂閱人數'+str(len(set(channelName_List))))
        Subscriptdict=dict(zip(channelID_List,channelName_List))
        SubscriptList.WriteFile(self,Subscriptdict)
        

    def WriteFile(self,Subscriptdict):
            with open(self.SavePath['channel_ListPath']+self.data['channelID'] +'.json', 'w') as f:
                json.dump(Subscriptdict, f)

