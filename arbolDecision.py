import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import joblib

dados = pd.read_csv('dados_tratados_final.csv')

colunas_excluir = ['Perfil_', 'Unidade_', 'Serie_', 'Curso_']
colunas_perguntas = [c for c in dados.columns if not any(p in c for p in colunas_excluir)]

dados_numericos = dados[colunas_perguntas].select_dtypes(include=['number']).astype(float)

dados['IndiceSatisfacao'] = dados_numericos.mean(axis=1)
dados = dados.dropna(subset=['IndiceSatisfacao'])

dados['ClasseSatisfacao'] = pd.cut(
    dados['IndiceSatisfacao'],
    bins=[0, 2.5, 3.5, 5],
    labels=['Baixa', 'Média', 'Alta']
).astype(str)

print("Distribuição das classes de satisfação:")
print(dados['ClasseSatisfacao'].value_counts())

X = dados.drop(columns=['IndiceSatisfacao', 'ClasseSatisfacao'])
y = dados['ClasseSatisfacao']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
modelo.fit(X_train, y_train)

plt.figure(figsize=(60,40)) 
plot_tree(
    modelo,
    feature_names=X.columns,
    class_names=modelo.classes_,
    filled=True,
    rounded=True,
    fontsize=10,
    max_depth=None 
)
plt.tight_layout()
plt.savefig("arvore_decisao_expandida.png", dpi=300)  
plt.show()

print("\n Árvore de decisão salva como 'arvore_decisao_corrigida.png'")
print("Acurácia no teste:", modelo.score(X_test, y_test))

importancias = pd.DataFrame({
    'Pergunta': X.columns,
    'Importancia': modelo.feature_importances_
}).sort_values(by='Importancia', ascending=False)

print("\nPrincipais variáveis que influenciam a satisfação:")
print(importancias.head(10))

joblib.dump(modelo, "modelo_satisfacao.pkl")
joblib.dump(X.columns.tolist(), "colunas_modelo.pkl")
print("Modelo e colunas salvos com sucesso!")