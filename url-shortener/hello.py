from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    #return "helloooo I'm still the homepage"
    return render_template('home.html', name='Coy')

@app.route('/about')
def about():
    return 'This is a url shortener from Linkedin Learning'