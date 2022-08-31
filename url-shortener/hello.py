from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "helloooo I'm still the homepage"

@app.route('/about')
def about():
    return 'This is a url shortener from Linkedin Learning'