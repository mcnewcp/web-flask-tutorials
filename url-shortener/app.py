from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import json
import os.path

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        #data stored in dictionary with key=short url, val=full url
        urls = {}

        #open json if it exists
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        
        #check if short url has been used
        if request.form['code'] in urls.keys():
            return redirect(url_for('home'))

        #write new data
        urls[request.form['code']] = {'url':request.form['url']}
        
        #write to json
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))