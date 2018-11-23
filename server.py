#!flask/bin/python
from flask import Flask, jsonify, request, render_template
import json,re
import threading
import pymysql
lock = threading.Lock()

# URL
# file:///home/willdoliver/Desktop/2018.2/Integrados/templates/front.html
app = Flask(__name__)

# ROTAS
# /clientes                 Retorna todos os clientes
# /cliente/*                Retorna todos os cartoes do cliente
# /cartao/*                 Retorna as movimentacoes do cartao

# Conecao com o BD
DSN = ('localhost','root','root','Tete',3306)
#DSN = ('200.134.10.221','wolverine','@wolverine#','wolverine',3306)
dw = pymysql.connect(*DSN,charset='utf8')
cursor = dw.cursor(pymysql.cursors.DictCursor)


########################################################################################
##############################  C L I E N T E S  #######################################
########################################################################################

# retorna todos os clientes
@app.route('/', methods=['GET'])
def get_home():
    return render_template("front.html")

# retorna todos os clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    global cursor

    select = "SELECT * FROM clientes"
    cursor.execute(select)
    rows = cursor.fetchall()
    
    return jsonify({'Clientes': rows})
    #return render_template("front.html", clientes=rows)

# retorna os cartoes do cliente
@app.route('/cliente/', methods=['GET'])
def get_cliente():
    cliente_id = request.args.get('id_cliente')

    cliente_id = int(cliente_id)
    print("Busca de cliente por ID")
    select = "SELECT id FROM cartao WHERE idfk_cliente = '%s'" % (cliente_id)
    cursor.execute(select)
    try:
        # retorna item indicado
        rows = cursor.fetchall()
        return render_template("front.html", cartoes=rows)
    except:
        # se nao encontrar retorna erro
        return jsonify({'error 404': 'Not found'})

# retorna os cartoes do cliente
@app.route('/cartao/', methods=['GET'])
def get_cartao():
    #5100858879155181
    cartao_id = request.args.get('id_cartao')
    dta_ini = request.args.get('ini_date')
    dta_fim = request.args.get('fim_date')

    print("Busca de movimentacoes pelo cartao")
    cartao_id = int(cartao_id)

    if (dta_ini == '' and dta_fim == ''):
        select = "SELECT data_mov, valor_mov, saldo_ini, saldo_fim FROM movimentacao WHERE idfk_cartao = '%s'" % (cartao_id)
        cursor.execute(select)
    
        try:
            # retorna item indicado
            rows = cursor.fetchall()
            print(rows)

            return render_template("front.html", movimentacoes=rows)
        except:
            # se nao encontrar retorna erro
            return jsonify({'error 404': 'Not found'})

    else:
        select = "SELECT data_mov, valor_mov, saldo_ini, saldo_fim FROM movimentacao WHERE idfk_cartao = '%s' and data_mov BETWEEN '%s' AND '%s' limit 100" % (cartao_id, dta_ini, dta_fim)
        #valor1 = "SELECT saldo_ini FROM movimentacao WHERE idfk_cartao = '%s' and data_mov >= '%s' limit 1;" % (cartao_id, dta_ini)
        #valor2 = "SELECT saldo_fim FROM movimentacao WHERE idfk_cartao = '%s' and data_mov <= '%s' order by id desc limit 1;" % (cartao_id, dta_fim)

        try:
            cursor.execute(select)
            rows = cursor.fetchall()
            
            return render_template("front.html", movimentacoes=rows)

            # cursor.execute(valor1)
            # v1 = cursor.fetchone()
            # v1 = v1.values()
            # v1 = v1.get('saldo_ini')
            # v1 = v1['saldo_ini']
            
            # cursor.execute(valor2)
            # v2 = cursor.fetchone()
            # #v2 = v2.values()
            # v2 = v2.get("saldo_fim")
            
            #saldo = v2-v1
            #print("saldo: "+ saldo)
            #return render_template("front.html", saldo=saldo)
        except:
            print("Erro ao calcular saldo")
            return jsonify({'error 404': 'Not found'})


# executa o servidor
if __name__ == '__main__':
    #global cursor 
    app.run(debug=True)




#################
# Trab 2
# Algoritmo BLAS
# 