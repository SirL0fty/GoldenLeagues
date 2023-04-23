from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sQ9kocDCG2kMAfrjsHAmBpxui3XkEa6ZQReTiqDd'

from app import routes 

# from dotenv import load_dotnev 

# load_dotnev()