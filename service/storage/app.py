from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

POSTGRES = {
    'user': 'postgres',
    'password': '4311',
    'db': 'YTstorage',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES

if __name__ == '__main__':
    app.run()
