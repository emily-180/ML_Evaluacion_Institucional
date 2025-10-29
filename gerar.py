import pandas as pd
import joblib

modelo = joblib.load("modelo_satisfacao.pkl")
dados = pd.read_csv("dados_tratados_final.csv")

colunas_excluir = ['Perfil_', 'Unidade_', 'Serie_', 'Curso_']
colunas_perguntas = [
    c for c in dados.columns
    if not any(p in c for p in colunas_excluir)
    and dados[c].dtype in ['float64', 'int64'] 
]

dados_numericos = dados[colunas_perguntas].astype(float)
dados["IndiceSatisfacao"] = dados_numericos.mean(axis=1)

dados["ClasseSatisfacao"] = pd.cut(
    dados["IndiceSatisfacao"],
    bins=[0, 2.5, 3.5, 5],
    labels=["Baixa", "Média", "Alta"]
).astype(str)

importancias = pd.DataFrame({
    "Pergunta": modelo.feature_names_in_,
    "Importancia": modelo.feature_importances_
})

remover = ["Curso_", "Unidade_", "Perfil_", "Serie_"]
importancias = importancias[~importancias["Pergunta"].str.contains("|".join(remover))]

importancias = importancias.sort_values(by="Importancia", ascending=False)

importancias = importancias.head(10)

importancias.to_csv("static/data/importancias.csv", index=False)
print("✅ Importâncias filtradas e top 10 geradas!")

colunas_cursos = [col for col in dados.columns if col.startswith("Curso_")]
media_por_curso = {}

for col in colunas_cursos:
    nome = col.replace("Curso_", "")
    subset = dados[dados[col] == 1]
    if not subset.empty:
        media_por_curso[nome] = subset["IndiceSatisfacao"].mean()

media_curso = pd.DataFrame({
    "Curso": list(media_por_curso.keys()),
    "Média": list(media_por_curso.values())
}).sort_values(by="Média", ascending=False)

media_curso.to_csv("static/data/media_curso.csv", index=False)
print("✅ 'media_curso.csv' gerado com sucesso!")

coluna_unidade = None
for c in dados.columns:
    if "Unidade_" in c or "unidade" in c.lower():
        coluna_unidade = c
        break

if coluna_unidade:
   
    unidades = [c for c in dados.columns if "Unidade_" in c]
    media_unidade = {}

    for u in unidades:
        nome = u.replace("Unidade_", "")
        subset = dados[dados[u] == 1]
        if not subset.empty:
            media_unidade[nome] = subset["IndiceSatisfacao"].mean()

    if media_unidade:
        media_unidade = pd.Series(media_unidade).sort_values(ascending=False)
        mais_satisfeito = media_unidade.idxmax()
        menos_satisfeito = media_unidade.idxmin()
    else:
        mais_satisfeito = menos_satisfeito = "Não disponível"
        media_unidade = {}
else:
    mais_satisfeito = menos_satisfeito = "Não disponível"
    media_unidade = {}

resultado = {
    "mais_satisfeito": mais_satisfeito,
    "menos_satisfeito": menos_satisfeito,
    "medias_unidades": media_unidade
}

joblib.dump(resultado, "resultado_unidades.pkl")

print("✅ Dados gerados com sucesso!")
print("Mais satisfeito:", mais_satisfeito)
print("Menos satisfeito:", menos_satisfeito)
