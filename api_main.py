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
        

@app.route('/cliente/<id>')
def get_cliente(id):
    return "O cliente solicitado foi " + str(id)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



