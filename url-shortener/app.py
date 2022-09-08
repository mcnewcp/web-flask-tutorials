from flask import Flask, render_template, request, redirect, flash
from flask.helpers import url_for
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'ea34i;lkjd42'

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
            flash('That short name has already been used.  You must select another short name.')
            return redirect(url_for('home'))

        #check if file or url
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            #ensure file is safe to save
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/mcnew/Documents/Projects/Github/web-flask-tutorials/url-shortener/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}
        #write to json
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            #look for key in dict
            if code in urls.keys():
                #if its a url, redirect
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])

                #if its a static file, get the address
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
                    