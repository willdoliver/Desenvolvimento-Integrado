import pymysql
from random import randint
import json
import time


array_cartao = []
total_cartao = 0

def conexao():
	global cur, conex 
	try:
		# CONEXAO SERVER RLE
		#conex = pymysql.connect(db= 'wolverine', user = 'wolverine', password = "@wolverine#", host = '200.134.10.221', port = 3306)
		# CONEXAO LOCALHOST
		conex = pymysql.connect(db= 'Tete', user = 'root', password = "root", host = 'localhost', port = 3306)
		cur = conex.cursor() #Abre um cursor para executar operações no BD

		print("****Conectou ao banco!****")
	except Exception as e:
		print("Erro ao conectar: ", e)

def insereCartao():
	global cur, conex
	total_cartao = 0
	inicio = time.time()
	for id_cliente in range(1,10001):
		qtde = randint(3,5)
		sql_update = "UPDATE clientes SET qtde_cartao = %i WHERE id_cliente = %i" % (qtde, id_cliente)
		try:
			# ATUALIZA A QUANTIDADE DE CARTAO NA COLUNA clientes.qtde_cartao
			cur.execute(sql_update)
			conex.commit()
		except Exception as e:
			print(e)
			continue

		for x in range(0,qtde):
			codigo = randint(100,999)
			vencimento = '2023-05-08'
			# 4 variáveis com 4 caracteres cada. id_cartao é a concatenação delas
			a = randint(1000,9999)
			b = randint(1000,9999)
			c = randint(1000,9999)
			d = randint(1000,9999)
			id_cartao = str(a) +str(b) +str(c)+ str(d)

			sql_insercao = "INSERT INTO cartao(id_cartao, idfk_cliente, cod_seg, data_vcto, saldo) VALUES ('%s','%d','%d','%s','%d')" % (id_cartao, id_cliente, codigo, vencimento,0)

			try:
				cur.execute(sql_insercao)
				conex.commit()
				total_cartao = total_cartao+1

			except Exception as e:
				print(e)
				continue

	fim = time.time()
	print("Tempo:", fim-inicio)
	return total_cartao


# FUNÇÃO PARA CRIAR UMA ARRAY COM OS IDS DOS CARTÕES E PARA SABER O TOTAL DE CARTÃO SEM TER QUE INSERIR TODOS NOVAMENTE
def arraycartao():
	global cur 
	try:
		cur.execute('SELECT id_cartao FROM cartao')
		for row in cur.fetchall():
		    array_cartao.append(row[0])

	except Exception as e:
		raise e

	print('Total de cartão: ',len(array_cartao))
	return len(array_cartao)



def insereMovimentacao(total):
	global cur, conex
	count = 0 
	fail = 0 
	inicio = time.time()
	#Criando transações e datas randomicas - 5 anos
	for ano in range(1,6):
		#Criando transações e datas randomicas - 12 meses
		for mes in range(1,13):
			# Laço de repetição para inserir 72bi de movimentações
			for x in range(1,30):				
				#Criando transações e datas randomicas - 1200 transações
				for transacao in range(0,25000):

					data_transacao = "20"+str(ano+14)+"-"+str(mes)+"-"+str(x)
					valor_movimentacao = str(randint(-1000, 1000))+ "." + str(randint(0,99))
					rand = randint(1,int(total))

					# CONSULTA O SALDO DO CARTAO ANTES DE EFETUAR A MOVIMENTAÇÃO
					saldo_atual = "SELECT saldo FROM cartao WHERE id = %i" % rand
					try:
						saldo_atual = cur.execute(saldo_atual)
						# DEVE TER OUTRA FORMA MAIS SIMPLES DE PEGAR O SALDO
						for linha in cur.fetchall():
							saldo_atual = linha[0]
					except Exception as e:
						print(e)
						continue


					saldo_fim = float(saldo_atual) + float(valor_movimentacao)
					# FAZ A MOVIMENTAÇÃO E EM SEGUIDA ATUALIZA O SALDO DO CARTÃO, EM cartao.saldo

					sql_insercao = "INSERT INTO movimentacao(data_mov, valor_mov, idfk_cartao, saldo_ini, saldo_fim) VALUES ('%s','%s','%s','%s','%s')" % (data_transacao,valor_movimentacao, rand, saldo_atual, saldo_fim)
					sql_atualiza = "UPDATE cartao SET saldo = %f WHERE id = %i" % (saldo_fim, rand)

					try:
						cur.execute(sql_insercao)
						cur.execute(sql_atualiza)
						conex.commit()

						count += 1
					except Exception as e:
						fail += 1
						continue
					if count == 100000 or count == 1000000 or count == 25000000 or count == 40000000 or count == 50000000:
						print(count, "movimentações inseridas...")

	fim = time.time()
	print("Tempo: ", fim-inicio)
	print(count, " dados inseridos\n", fail, " nao inseridos")


if __name__ == '__main__':
	conexao()
	a = insereCartao()
	print("%d cartoes inseridos" % a)
	#a = arraycartao() #usar essa função quando quiser saber o total de cartão inserido sem ter que chamar a função insereCartao() novamente. Deixar comentada como default
	insereMovimentacao(a)



	#############################################
		# SQL: clientes com mais transações realizadas.
# SELECT movimentacao.idfk_cartao, clientes.nome_cliente, count(*) FROM wolv.movimentacao, wolv.clientes  WHERE movimentacao.idfk_cartao = clientes.id_cliente group by(movimentacao.idfk_cartao) order by(count(*)) desc;

	

	#############################################
		# GERAR TABELAS NO WORKBENCH

# CREATE TABLE `cartao` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `id_cartao` varchar(20) DEFAULT NULL,
#   `idfk_cliente` int(11) DEFAULT NULL,
#   `cod_seg` int(11) DEFAULT NULL,
#   `data_vcto` date DEFAULT NULL,
#   `saldo` float DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=MyISAM AUTO_INCREMENT=40068 DEFAULT CHARSET=latin1;


# CREATE TABLE `movimentacao` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `data_mov` date DEFAULT NULL,
#   `valor_mov` float DEFAULT NULL,
#   `idfk_cartao` varchar(45) DEFAULT NULL,
#   `saldo_ini` float DEFAULT NULL,
#   `saldo_fim` float DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=MyISAM AUTO_INCREMENT=174230 DEFAULT CHARSET=latin1;


# CREATE TABLE `clientes` (
#   `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
#   `nome_cliente` varchar(45) NOT NULL,
#   `data_nasc` date NOT NULL,
#   `email` varchar(45) NOT NULL,
#   `endereco` varchar(45) NOT NULL,
#   `cep` varchar(16) NOT NULL,
#   `qtde_cartao` int(11) DEFAULT NULL,
#   PRIMARY KEY (`id_cliente`)
# ) ENGINE=InnoDB AUTO_INCREMENT=10001 DEFAULT CHARSET=latin1;

