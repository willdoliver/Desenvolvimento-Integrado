import pymysql
from random import randint

id_cartao = []	
data_transacao = []
valor_movimentacao = []

def conexao():
	global cur, conex 
	try:
		# CONEXAO SERVER RLE
		conex = pymysql.connect(db= 'wolverine', user = 'wolverine', password = "@wolverine#", host = '200.134.10.221', port = 3306)
		# CONEXAO LOCALHOST
		#conex = pymysql.connect(db= 'wolv', user = 'root', password = "", host = '127.0.0.1', port = 3306)

		cur = conex.cursor() #Abre um cursor para executar operações no BD
		print("****Conectou ao banco!****")
	except Exception as e:
		print("Erro ao conectar: ", e)


def arraycartao():
	global cur 
	try:
		cur.execute('SELECT id_cartao FROM cartoes')
		for row in cur.fetchall():
		    id_cartao.append(row[0])

	except Exception as e:
		raise e

def insereMovimentacao():
	global cur, conex
	cont = 0 
	fail = 0 

	#Criando transações e datas randomicas - 5 anos
	for ano in range(1,6):
		#Criando transações e datas randomicas - 12 meses
		for mes in range(1,13):
			#Criando transações e datas randomicas - 1200 transações
			for transacao in range(0,1500):
				data_transacao = "20"+str(ano+14)+"-"+str(mes)+"-"+str(randint(1,30))
				valor_movimentacao = str(randint(-1000, 1000))+ "." + str(randint(0,99))
				x = randint(0,40099)
				idfk_cartao = id_cartao[x]

				try:
					sql_insercao = "INSERT INTO movimentacoes(data_mov, valor_mov, idfk_cartao) VALUES ('%s','%s','%s')" % (data_transacao,valor_movimentacao, idfk_cartao)
					cur.execute(sql_insercao)
					conex.commit()
					cont += 1
				except Exception as e:
					fail += 1
					continue
				print(cont, " de 90000")
	print(cont, " dados inseridos\n", fail, " nao inseridos")


if __name__ == '__main__':
	conexao()
	arraycartao()
	insereMovimentacao()
