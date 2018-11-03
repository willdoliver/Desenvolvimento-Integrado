######################
#'		SCHEMA INFORMATION'
#  CLIENTES(id_cliente(PK), nome_cliente, data_nasc, email, endereço, cep)
#  CARTAO(ID(pk), id_cartao, idfk_cliente, cod_seg, data_vcto, saldo)
#  MOVIMENTACAO(id(pk), data_mov, valor_mov, idfk_cartao, saldo_ini, saldo_fim)
######################


import pymysql
from random import randint
import json
import time

id_cartao = []	
data_transacao = []
valor_movimentacao = []

def conexao():
	global cur, conex 
	try:
		# CONEXAO SERVER RLE
		#conex = pymysql.connect(db= 'wolverine', user = 'wolverine', password = "@wolverine#", host = '200.134.10.221', port = 3306)
		# CONEXAO LOCALHOST
		conex = pymysql.connect(db= 'wolv', user = 'root', password = "", host = '127.0.0.1', port = 3306)

		cur = conex.cursor() #Abre um cursor para executar operações no BD
		print("****Conectou ao banco!****")
	except Exception as e:
		print("Erro ao conectar: ", e)

def insereCartao():
	inicio = time.time()
	for id_cliente in range(1,10000):
		qtde = randint(3,5)
		# CADA CLIENTE TEM DE 3 A 5 CARTOES
		for x in range(0,qtde):
			codigo = randint(111,999)
			vencimento = '2023-05-08'
			# 4 variáveis com 4 caracteres cada. id_cartao é a concatenação delas
			a = randint(1000,9999)
			b = randint(1000,9999)
			c = randint(1000,9999)
			d = randint(1000,9999)
			id_cartao = str(a) +str(b) +str(c)+ str(d)

			try:
				sql_insercao = "INSERT INTO CARTAO(id_cartao, idfk_cliente, cod_seg, data_vcto, saldo) VALUES ('%s','%d','%d','%s','%d')" % (id_cartao, id_cliente, codigo, vencimento,0)
				cur.execute(sql_insercao)
				conex.commit()
			except Exception as e:
				print(e)
				continue
	fim = time.time()
	print("Tempo: ", fim-inicio)


def arraycartao():
	global cur 
	try:
		cur.execute('SELECT id_cartao FROM cartao')
		for row in cur.fetchall():
		    id_cartao.append(row[0])

	except Exception as e:
		raise e

	print('Total de cartão: ',len(id_cartao))

def insereMovimentacaoOLD():
	global cur, conex
	cont = 0 
	fail = 0 
	inicio = time.time()
	#Criando transações e datas randomicas - 5 anos
	for ano in range(1,6):
		#Criando transações e datas randomicas - 12 meses
		for mes in range(1,13):
			#for x in range(1,10000):				
			#Criando transações e datas randomicas - 1200 transações
			for transacao in range(0,1200):
				data_transacao = "20"+str(ano+14)+"-"+str(mes)+"-"+str(randint(1,30))
				valor_movimentacao = str(randint(-1000, 1000))+ "." + str(randint(0,99))
				num = randint(0,40099)
				#idfk_cartao = id_cartao[num]
					## EM CADA INSERÇÃO, ATUALIZAR A COLUNA/TABELA DE SALDO, DE ACORDO COM O ID DO CARTÃO
				try:
					sql_insercao = "INSERT INTO movimentacoes(data_mov, valor_mov, idfk_cartao) VALUES ('%s','%s','%s')" % (data_transacao,valor_movimentacao, "idfk_cartao")
					cur.execute(sql_insercao)
					conex.commit()
					cont += 1
				except Exception as e:
					fail += 1
					continue
	fim = time.time()
	print("Tempo: ", fim-inicio)
	print(cont, " dados inseridos\n", fail, " nao inseridos")


def insereMovimentacao():
	
	global cur, conex
	cont = 0 
	fail = 0 
	inicio = time.time()

	#Criando transações e datas randomicas - 5 anos
	for ano in range(1,6):
		#Criando transações e datas randomicas - 12 meses
		for mes in range(1,13):
			data_transacao = "20"+str(ano+14)+"-"+str(mes)+"-"+str(randint(1,30))
			valor_movimentacao = str(randint(-1000, 1000))+ "." + str(randint(0,99))
			num = randint(0,40099)
			
			saldo_atual = "SELECT saldo FROM cartao WHERE id = %i" % num
			saldo_atual = cur.execute(saldo_atual)

			for linha in cur.fetchall():
				saldo_atual = linha[0]

			saldo_fim = float(saldo_atual) + float(valor_movimentacao)
			sql_mov = "INSERT INTO movimentacao(data_mov, valor_mov, idfk_cartao, saldo_ini, saldo_fim) VALUES ('%s','%s','%s','%s','%s')" % (data_transacao,valor_movimentacao, num, saldo_atual, saldo_fim)
			sql_atualiza = "UPDATE cartao SET saldo = %f WHERE id = %i" % (saldo_fim, num)


	fim = time.time()
	print("Tempo: ", fim-inicio)
	f.close()




if __name__ == '__main__':
	conexao()
	#arraycartao()
