from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')
app.static_url_path = '/static'


# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'concessionaria'

mysql = MySQL(app)

@app.route('/')
def index():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM veiculos")
    veiculos = cur.fetchall()
    cur.close()
    return render_template('index.html', veiculos=veiculos)

@app.route('/adicionar_veiculo', methods=['POST'])
def adicionar_veiculo():
    if request.method == 'POST':
        dados = request.form
        tipo = dados['tipo']
        cor = dados['cor']
        marca = dados['marca']
        modelo = dados['modelo']
        ano_fabricacao = int(dados['ano_fabricacao'])
        estado = dados['estado']
        km_rodados = int(dados['km_rodados'])
        passagem_por_leilao = bool(int(dados['passagem_por_leilao']))
        formas_pagamento = dados['formas_pagamento']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO veiculos (tipo, cor, marca, modelo, ano_fabricacao, estado, km_rodados, passagem_por_leilao, formas_pagamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (tipo, cor, marca, modelo, ano_fabricacao, estado, km_rodados, passagem_por_leilao, formas_pagamento)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/excluir_veiculo/<int:id>')
def excluir_veiculo(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM veiculos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/editar_veiculo/<int:id>', methods=['POST', 'GET'])
def editar_veiculo(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        dados = request.form
        tipo = dados['tipo']
        cor = dados['cor']
        marca = dados['marca']
        modelo = dados['modelo']
        ano_fabricacao = int(dados['ano_fabricacao'])
        estado = dados['estado']
        km_rodados = int(dados['km_rodados'])
        passagem_por_leilao = bool(int(dados['passagem_por_leilao']))
        formas_pagamento = dados['formas_pagamento']

        cur.execute(
            "UPDATE veiculos SET tipo=%s, cor=%s, marca=%s, modelo=%s, ano_fabricacao=%s, estado=%s, km_rodados=%s, passagem_por_leilao=%s, formas_pagamento=%s WHERE id=%s",
            (tipo, cor, marca, modelo, ano_fabricacao, estado, km_rodados, passagem_por_leilao, formas_pagamento, id)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM veiculos WHERE id = %s", (id,))
        veiculo = cur.fetchone()
        cur.close()
        return render_template('editar.html', veiculo=veiculo)

if __name__ == '__main__':
    app.run(debug=True)
