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

@app.route("/negocio")
def negocio():
    return render_template("negocio.html")

@app.route("/datos")
def datos():
    return render_template("datos.html")
