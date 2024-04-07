def application_run(text):
    from flask import Flask, render_template
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('index.html', string_in = text)
    app.run(debug=True)