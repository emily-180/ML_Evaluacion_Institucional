import pandas as pd

dados = pd.read_csv("static/data/[Cópia] Questionario 2024_2 - Base Formatada.csv")

escala_geral = {
    "discordo plenamente": 1,
    "discordo": 2,
    "não concordo nem discordo": 3,
    "não concordo, nem discordo": 3,
    "concordo": 4,
    "concordo plenamente": 5,
    "não": 1,
    "sim": 2,
    "parcialmente": 2,
    "não sei dizer": 0,
    "prefiro não responder": 0,
    "muito ruim": 1,
    "muito ruins": 1,
    "ruim": 2,
    "ruins": 2,
    "regular": 3,
    "regulares": 3,
    "boa": 4,
    "muito boa": 5,
    "boas": 4,
    "muito boas": 5,
    "bom": 4,
    "muito bom": 5,
    "bons": 4,
    "muito bons": 5,
    "bons/boas": 4,
    "muito bons/boas": 5,
    "bom/boa": 4,
    "muito bom/boa": 5,
    "totalmente ineficiente": 1,
    "ineficiente": 2,
    "nem eficiente e nem ineficiente": 3,
    "eficiente": 4,
    "totalmente eficiente": 5,
    "totalmente imperceptível": 1,
    "imperceptível": 2,
    "não é perceptível nem imperceptível": 3,
    "perceptível": 4,
    "totalmente perceptível": 5,
    "não sei responder": 0,
    "não sei": 0,
    "prefiro não responder": 0,
    "não se aplica": 0
}

dados = dados.applymap(
    lambda x: escala_geral.get(str(x).strip().lower(), x) if isinstance(x, str) else x
)

dados = pd.get_dummies(dados, columns=['Perfil', 'Unidade', 'Serie', 'Curso'], drop_first=True)

print(dados.head())

dados.to_csv('dados_tratados.csv', index=False)

print("Arquivo 'dados_tratados.csv' gerado com sucesso!")
