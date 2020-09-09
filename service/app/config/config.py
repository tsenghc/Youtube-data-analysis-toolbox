import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    try:
        API_DEVELOPER_KEY = os.environ["DEVELOPER_KEY"]
    except KeyError:
        print(KeyError)
        # The API_DEVELOPER_KEY is YouTube_Data_API_v3_key
        API_DEVELOPER_KEY = ""


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES = {
        'user': 'postgres',
        'password': '4311',
        'db': 'YTstorage',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES


config = {
    'development': DevelopmentConfig,

}
