from flask import render_template, request
from app import app 
from app.forms import ContactForm

@app.route('/', methods=['GET', 'POST'])
def index():
    # error = ""

    form = ContactForm()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        # if len(name) == 0 or len(email) == 0 or len(message) == 0:
        # error =  "Please supply all information"
        
    # return "Thank You for Your message."
        
            return render_template('index.html', form=form)


@app.route('/tennis')
def tennis():
        return render_template('tennis.html')
# @app.route('/home')
# def home():
#     return render_template ('home.html', title='home')