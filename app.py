from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
        return render_template('index.html', footer='footer.html')


if __name__ == '__main__':
        app.run(debug=True, port=5050, host='0.0.0.0')
