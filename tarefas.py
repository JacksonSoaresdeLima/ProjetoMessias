import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente
os.environ['FLASK_DEBUG'] = 'True'

# Configurando o modo de depuração com base na variável de ambiente
app.debug = os.environ.get('FLASK_DEBUG') == 'True'

@app.route('/')
def ola():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/tarefas')
def tarefas():

    lista_de_tarefas = []

    with open(
            'bd_tarefas.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            lista_de_tarefas.append(l)

    return render_template('glossario.html',
                           tarefas=lista_de_tarefas)


@app.route('/nova_tarefa')
def novo_tarefas():
    return render_template('adicionar_tarefas.html')


@app.route('/criar_tarefas', methods=['POST', ])
def criar_tarefas():
    tarefas = request.form['tarefas']
    definicao = request.form['definicao']

    with open(
            'bd_tarefas.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([tarefas, definicao])

    return redirect(url_for('tarefas'))


@app.route('/excluir_tarefas/<int:tarefa_id>', methods=['POST'])
def excluir_tarefas(tarefa_id):

    with open('bd_tarefas.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == tarefas_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_tarefas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('tarefas'))


if __name__ == "__main__":
    app.run()