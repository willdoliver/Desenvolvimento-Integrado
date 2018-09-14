#!flask/bin/python
from flask import Flask, jsonify, request
import json,re
import threading
import pymysql
from Levenshtein import distance
lock = threading.Lock()

app = Flask(__name__)

# URLs

# /bandas                   Retorna todas as Bandas
# /filmes                   Retorna todos os Filmes
# /bandas/id                Retorna Banda especifica
# /filmes/id                Retorna Filme especifico
# /insereBanda/             Insere nova Banda
# /insereFilme/             Insere novo Filme


DSN = ('localhost','root','root','top',3306)
dw = pymysql.connect(*DSN,charset='utf8')
cursor = dw.cursor(pymysql.cursors.DictCursor)


########################################################################################
################################  B A N D A S  #########################################
########################################################################################

# mostra todas as vendas de passagens aereas
@app.route('/bandas', methods=['GET'])
def get_bandas():
    global cursor
    # Mudar para a tabela bandas
    select = "SELECT * FROM musicas"
    cursor.execute(select)
    rows = cursor.fetchall()
    return jsonify({'Bandas': rows})

# mostra compras de passagem por id
@app.route('/bandas/', methods=['GET'])
def get_banda():
    notas = {}
    banda_id = request.args.get('id_banda_cantor')

    try:
        banda_id = int(banda_id)
        print("Busca por ID")
        select = "SELECT * FROM musicas WHERE id_banda = '%s'" % (banda_id)
        cursor.execute(select)
        try:
            # retorna item indicado
            rows = cursor.fetchall()
            return jsonify({'Banda': rows})
        except:
            # se nao encontrar retorna erro
            return jsonify({'error 404': 'Not found'})
    except:
        print("Busca por TEXTO")
        select = "SELECT nome FROM top.musicas ORDER BY nome"
        cursor.execute(select)
        bd_name = cursor.fetchone()

        while(bd_name):
            nome_banda = bd_name['nome']
            banda = unicode(banda_id)

            dist = distance(banda, nome_banda)
            print(dist, nome_banda)
            notas[nome_banda] = dist
            bd_name = cursor.fetchone()
        nota_max = min(notas, key=notas.get)

        select = "SELECT * FROM musicas WHERE nome = '%s'" % (nota_max)
        cursor.execute(select)
        try:
            # retorna item indicado
            rows = cursor.fetchall()
            return jsonify({'Banda': rows})
        except:
            # se nao encontrar retorna erro
            return jsonify({'error 404': 'Not found'})

# Insere uma nova compra de voo
@app.route('/insereBanda/', methods=['GET'])
def get_cadastro_banda():
    lock.acquire()
    # captura dados informados pelo cliente
    bandaCantor = request.args.get('banda_cantor')
    genero = request.args.get('genero')
    pais = request.args.get('pais')
    tipo = request.args.get('tipo')
    dataIni = request.args.get('dataIni')
    dataFim = request.args.get('dataFim')

    print(bandaCantor)
    print(genero)
    print(pais)
    print(tipo)
    print(dataIni)
    print(dataFim)

    try:
        sql_insercao = "INSERT INTO musicas (nome,genero,pais,tipo,data_begin,date_end) VALUES ('%s','%s','%s','%s','%s','%s')" % (bandaCantor,genero,pais,tipo,dataIni,dataFim)
        cursor.execute(sql_insercao)
        dw.commit()
        lock.release()
        return "Banda cadastrada com sucesso :)"
    except:
        lock.release()
        return "Erro na insercao da banda :("

########################################################################################
################################  F I L M E S   ########################################
########################################################################################

# mostra todas as reservas de hotel
@app.route('/filmes', methods=['GET'])
def get_filmes():
    global cursor
    # Mudar para a tabela filmes
    select = "SELECT * FROM filmes"
    cursor.execute(select)
    rows = cursor.fetchall()
    return jsonify({'Filmes': rows})

# mostra reservas por id
@app.route('/filmes/', methods=['GET'])
def get_filme():
    notas = {}
    id_filme = request.args.get('id_filme')

    try:
        id_filme = int(id_filme)
        print("Busca por ID")
        select = "SELECT * FROM filmes WHERE id_filme = '%s'" % (id_filme)
        cursor.execute(select)
        try:
            # retorna item indicado
            rows = cursor.fetchall()
            return jsonify({'Filme': rows})
        except:
            # se nao encontrar retorna erro
            return jsonify({'error 404': 'Not found'})

    except: 
        print("Busca por TEXTO")
        select = "SELECT nome_filme FROM top.filmes ORDER BY nome_filme"
        cursor.execute(select)
        bd_name = cursor.fetchone()

        while(bd_name):
            nome_filme = bd_name['nome_filme']
            filme = unicode(id_filme)

            dist = distance(filme, nome_filme)
            print(dist, nome_filme)
            notas[nome_filme] = dist
            bd_name = cursor.fetchone()
        nota_max = min(notas, key=notas.get)
        
        select = "SELECT * FROM filmes WHERE nome_filme = '%s'" % (nota_max)
        cursor.execute(select)
        try:
            # retorna item indicado
            rows = cursor.fetchall()
            return jsonify({'Filme': rows})
        except:
            # se nao encontrar retorna erro
            return jsonify({'error 404': 'Not found'})

# Insere uma nova reserva de hotel
@app.route('/insereFilme/', methods=['GET'])
def get_cadastro_filme():
    lock.acquire()

    # captura dados informados pelo cliente
    urlFilme = request.args.get('url_filme')
    nomeFilme = request.args.get('nome')
    genero = request.args.get('genero')
    data_lanc = request.args.get('dataLanc')
    produtora = request.args.get('produtora')
    notaFilme = request.args.get('nota')
    diretor = request.args.get('diretor')

    print(urlFilme)
    print(nomeFilme)
    print(genero)
    print(data_lanc)
    print(produtora)
    print(notaFilme)
    print(diretor)

    try:
        sql_insercao = "INSERT INTO filmes (url,nome_filme,rating,genero,produtora,data_lanc,diretor) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (urlFilme,nomeFilme,notaFilme,genero,produtora,data_lanc,diretor)
        cursor.execute(sql_insercao)
        dw.commit()
        lock.release()
        return "Filme cadastrado com sucesso :)"
    except:
        lock.release()
        return "Erro na insercao da banda :("

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    data_list = []
    value = request.args.get('genero')
    sql = "SELECT distinct genero FROM top.musicas;"
    cursor.execute(sql)
    cur = cursor.fetchone()
    while cur is not None:
        data_list.append(cur['genero'])
        cur = cursor.fetchone()
    #print(data_list)
    return jsonify(autocomplete=data_list)

# executa o servidor
if __name__ == '__main__':
    global cursor 
    app.run(debug=True)