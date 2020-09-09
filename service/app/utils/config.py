import os

try:
    API_DEVELOPER_KEY = os.environ["DEVELOPER_KEY"]
except KeyError:
    print(KeyError)
    # The API_DEVELOPER_KEY is YouTube_Data_API_v3_key
    API_DEVELOPER_KEY = ""
