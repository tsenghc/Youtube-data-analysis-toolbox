import os

try:
    API_DEVELOPER_KEY = os.environ["DEVELOPER_KEY"]
except KeyError:
    print(KeyError)
    # The API_DEVELOPER_KEY is YouTube_Data_API_v3_key
    API_DEVELOPER_KEY = ""

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
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 280,
                                 'pool_timeout': 100, 'pool_pre_ping': True}

    POSTGRES = {
        'user': '',
        'password': '',
        'db': '',
        'host': '',
        'port': '',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES


app_config = {
    'development': DevelopmentConfig,
}
