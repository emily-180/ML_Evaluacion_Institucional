import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import joblib

dados = pd.read_csv('dados_tratados_final.csv')

colunas_excluir = ['Perfil_', 'Unidade_', 'Serie_', 'Curso_']
colunas_perguntas = [c for c in dados.columns if not any(p in c for p in colunas_excluir)]

dados_numericos = dados[colunas_perguntas].select_dtypes(include=['number']).astype(float)

dados['IndiceSatisfacao'] = dados_numericos.mean(axis=1)

dados['ClasseSatisfacao'] = pd.cut(
    dados['IndiceSatisfacao'],
    bins=[0, 2.5, 3.5, 5],
    labels=['Baixa', 'Média', 'Alta']
).astype(str)

dados = dados[dados['ClasseSatisfacao'].isin(['Baixa', 'Média', 'Alta'])].reset_index(drop=True)

print("Classes únicas depois da limpeza:", dados['ClasseSatisfacao'].unique())

X = dados[colunas_perguntas]
y = dados['ClasseSatisfacao']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
modelo.fit(X_train, y_train)

plt.figure(figsize=(60, 40))
plot_tree(modelo, feature_names=X.columns, class_names=modelo.classes_, filled=True, rounded=True, fontsize=10)
plt.tight_layout()
plt.savefig("arvore_decisao_corrigida.png", dpi=300)
plt.show()

y_pred = modelo.predict(X_test)

print("\n📌 ACURÁCIA:", round(accuracy_score(y_test, y_pred), 4))
print("\n📌 CLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred))

mat_confusao = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 4))
sns.heatmap(mat_confusao, annot=True, fmt="d", cmap="Blues",
            xticklabels=modelo.classes_,
            yticklabels=modelo.classes_)
plt.title("Matriz de Confusão — Classificação de Satisfação")
plt.xlabel("Classe Prevista")
plt.ylabel("Classe Real")
plt.tight_layout()
plt.savefig("matriz_confusao.png", dpi=300)
plt.show()

importancias = pd.DataFrame({
    'Pergunta': X.columns,
    'Importancia': modelo.feature_importances_
}).sort_values(by='Importancia', ascending=False)

print("\nPrincipais variáveis que influenciam a satisfação:")
print(importancias.head(10))

joblib.dump(modelo, "modelo_satisfacao.pkl")
joblib.dump(X.columns.tolist(), "colunas_modelo.pkl")
print("Modelo e colunas salvos com sucesso!")
