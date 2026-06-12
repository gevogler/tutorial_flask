"""
[Aplicación básica del microframework Flask de Python]
Author: Georgina Vogler
Date: 2026-06-12
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/contacto")
def contacto():
    return render_template("base.html")