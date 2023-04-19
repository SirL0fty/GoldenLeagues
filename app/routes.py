from flask import render_template, request
from app import app 
from app.forms import ContactForm

@app.route('/', methods=['GET', 'POST'])
def index():
    
    form = ContactForm()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        message = form.message.data


        return "Thank You for Your message."
        
    return render_template('index.html', form=form)


@app.route('/tennis')
def tennis():
        return render_template('tennis.html')