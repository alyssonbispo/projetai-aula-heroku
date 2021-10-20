import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__) 


@app.route('/', methods=['GET', 'POST'])  # DEFAULT É SÓ GET
def minha_funcao():
    print(request.args.get('Valor'))
    my_params = request.args
    if(request.method == 'POST'):
        return ("Usuário sem permissão")
    return jsonify({"message": "Sorria você está sendo filmado!"})

@app.route('/testingcicd', methods=['GET'])  # DEFAULT É SÓ GET
def testingcicd_func():
    return jsonify({"message": "CI/CD feito com sucesso"})

@app.route('/novorecurso', methods=['GET', 'POST']) 
def novo_recurso():
    print(request.args.get('Valor'))
    
    if(request.method == 'POST'):
        my_params = request.form
    else: #get
        my_params = request.args

    if(my_params.get('Valor', type=int) == 42):
        return jsonify({"Valor": "O valor recebido foi: "
        +str(my_params.get('Valor', type=int))})
    else:
        return 'bad request!', 400


@app.route('/criatabelas', methods=['GET']) 
def criar_tabelas():
    commands = (
        """
        CREATE TABLE clientes (
            cliente_id SERIAL PRIMARY KEY,
            cliente_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE produtos (
                produto_id SERIAL PRIMARY KEY,
                produto_nome VARCHAR(255) NOT NULL
                )
        """)

    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    # create table one by one
    for command in commands:
        cur.execute(command)
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
    return 'Tabelas criadas!', 200

@app.route('/cliente', methods=['POST','GET']) 
def cliente_func():

    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()

    if(request.method == 'POST'):
        my_params = request.form
        cur.execute("INSERT INTO clientes (cliente_name) VALUES(%s) ",(my_params.get("nome"),))
        cur.close()
        conn.commit()
        return 'Usuário inserido', 200
    else: #get
        my_params = request.args
        cur.execute("SELECT * FROM clientes")
        mobile_records = cur.fetchall()
        for row in mobile_records:
            print("Id = ", row[0], )
            print("Nome = ", row[1], "\n")
        cur.close()
        return jsonify(mobile_records),200

@app.route('/cliente/<id>')
def get_cliente(id):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes WHERE cliente_id=%s ",(id,))
    mobile_records = cur.fetchall()
    for row in mobile_records:
        print("Id = ", row[0], )
        print("Nome = ", row[1], "\n")
    
    cur.close()
    # commit the changes
    conn.commit()
    return jsonify(mobile_records),200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



