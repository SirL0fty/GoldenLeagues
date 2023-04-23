from flask import render_template, request
from app import app 
from app.forms import ContactForm

@app.route('/', methods=['GET', 'POST'])
def index():
        return render_template('index.html')


@app.route('/tennis')
def tennis():
        return render_template('tennis.html')
# @app.route('/home')
# def home():
#     return render_template ('home.html', title='home')