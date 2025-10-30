from flask import Flask, render_template, redirect, session, url_for, request, jsonify
import joblib
import pandas as pd

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

@app.route("/interacion")
def interacion():
    return render_template("interacion.html")

modelo = joblib.load("modelo_satisfacao.pkl")
colunas_modelo = joblib.load("colunas_modelo.pkl")

@app.route("/prever", methods=["POST"])
def prever():
    dados = request.json

    entrada = pd.DataFrame([dados])

    for col in ["curso", "campus", "perfil"]:
        for c in colunas_modelo:
            if c.startswith(f"{col}_") and dados.get(col) == c[len(col)+1:]:
                entrada[c] = 1
            elif c.startswith(f"{col}_"):
                entrada[c] = 0

    for chave, valor in dados.items():
        if chave not in ["curso", "campus", "perfil"]:
            entrada[chave] = int(valor) if valor is not None else 0

    colunas_faltando = [col for col in colunas_modelo if col not in entrada.columns]
    entrada = pd.concat([entrada, pd.DataFrame(0, index=entrada.index, columns=colunas_faltando)], axis=1)

    entrada = entrada[colunas_modelo]
    predicao = modelo.predict(entrada)[0]

    return jsonify({"resultado": predicao})

@app.route("/analise")
def analise():
    importancias = pd.read_csv("static/data/importancias.csv")
    media_curso = pd.read_csv("static/data/media_curso.csv")

    resultado_unidades = joblib.load("resultado_unidades.pkl")
    medias_unidades = resultado_unidades["medias_unidades"]
    campus_mais = resultado_unidades["mais_satisfeito"]
    campus_menos = resultado_unidades["menos_satisfeito"]

    return render_template(
        "analise.html",
        importancias=importancias.to_dict(orient="records"),
        media_curso=media_curso.set_index("Curso")["Média"].to_dict(),
        medias_unidades=medias_unidades.to_dict(),  
        campus_mais=campus_mais,
        campus_menos=campus_menos
    )

