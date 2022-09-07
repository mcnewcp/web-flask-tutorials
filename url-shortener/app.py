from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import json

app = Flask(__name__)

@app.route('/')
def home():
    #return "helloooo I'm still the homepage"
    return render_template('home.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        #make a dictionary with key=short url, val=full url
        urls = {}
        urls[request.form['code']] = {'url':request.form['url']}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))