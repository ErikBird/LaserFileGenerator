from flask import Flask
from instance.config import Config
app = Flask(__name__)

if Config.ENV == "PRODUCTION":
    app.config.from_object('instance.config.ProductionConfig')
elif Config.ENV == "DEVELOPMENT":
    app.config.from_object('instance.config.DevelopmentConfig')


from app.views import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=False)

