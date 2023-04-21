from flask import Flask

app = Flask(__name__)

from app import routes 

# from dotenv import load_dotnev 

# load_dotnev()