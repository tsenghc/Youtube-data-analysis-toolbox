import os
import sys

try:
    API_DEVELOPER_KEY = os.environ["DEVELOPER_KEY"]
except KeyError:
    print("Please check environ variable")
    print("BaseConfig:{}".format(KeyError))
    sys.exit()
    # The API_DEVELOPER_KEY is YouTube_Data_API_v3_key

app_dir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig():
    try:
        POSTGRES = eval(os.environ['POSTGRES_CONFIG'])
    except KeyError:
        print("Please check environ variable")
        sys.exit()

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 280,
                                 'pool_timeout': 100, 'pool_pre_ping': True}
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES


app_config = {
    'development': DevelopmentConfig,
}
