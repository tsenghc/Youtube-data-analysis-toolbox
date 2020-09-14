import googleapiclient.discovery

from app.utils.config import API_DEVELOPER_KEY

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=API_DEVELOPER_KEY)
