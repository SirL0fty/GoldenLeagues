from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def index():
        return render_template('index.html')


@app.route('/tennis')
def tennis():
        return render_template('tennis.html')


if __name__ == '__main__':
        app.run(debug=True, port=5050, host='0.0.0.0')
