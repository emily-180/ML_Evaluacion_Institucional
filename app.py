from flask import Flask, render_template, redirect, session, url_for

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

