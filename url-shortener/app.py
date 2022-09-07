from flask import Flask, render_template, request, redirect
from flask.helpers import url_for

app = Flask(__name__)

@app.route('/')
def home():
    #return "helloooo I'm still the homepage"
    return render_template('home.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))