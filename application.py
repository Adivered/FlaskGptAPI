from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from config import DevConfig, ProdConfig

load_dotenv()

app = Flask(__name__)
CORS(app)
tmp_env = os.getenv("FLASK_ENV")

if tmp_env == "production":
    app.config.from_object(ProdConfig)
elif tmp_env == "development":
    app.config.from_object(DevConfig)

db = SQLAlchemy(app)

from View import main
