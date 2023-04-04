from flask import Flask, render_template

def run_app():
        app = Flask(__name__)
        app.run(debug=True, port=5050, host='0.0.0.0')

        @app.route('/', methods=['GET', 'POST'])
        def index():
                return render_template('index.html', footer='footer.html')

        return app