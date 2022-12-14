from flask import render_template, request, redirect, flash, abort, session, jsonify, Blueprint
from flask.helpers import url_for
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@bp.route('/your-url', methods=['GET', 'POST'])
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
            return redirect(url_for('urlshort.home'))

        #check if file or url
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            #ensure file is safe to save
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/mcnew/Documents/Projects/Github/web-flask-tutorials/url-shortener/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}
        #write to json
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))

@bp.route('/<string:code>')
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
        
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
