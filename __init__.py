from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from item-catalog-app import views
