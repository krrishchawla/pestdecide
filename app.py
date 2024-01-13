from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/explore_form')
def explore_form():
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
