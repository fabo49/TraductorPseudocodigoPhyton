# Universidad de Costa Rica
# Escuela de Ciencas de la Computacion e Informatica
# Automatas y Compiladores
# - Fabian Rodriguez
# - Abraham Vega
# I Semestre 2015
# -----------------------------------------------------------
# |		El programa traduce de un pseudocodigo a python		|
# -----------------------------------------------------------

# lexer

tokens = ('COMA', 'VAR', 'FIN', 'IF', 'WHILE', 'FOR', 'ELSE', 'IN', 'PARENA', 'PARENC', 'OPBIN', 'OPUNA', 'ASK', 'PRINT', 'ASIG', 'NUM', 'ID', 'PROC', 'EXPBOOL', 'COMENT', 'TAB', 'STRING', 'RETURN')

m_tabs = 0 	# variable global que lleva cuantos tabs se hicieron en cada linea
m_result = ""
m_totLineas = 1
m_reporte = ""

def t_coma(t):
	r','
	return t

def t_fin(t):
	r'fin'
	t.value = ''
	return t

def t_var(t):
	r'var'
	t.value = ''
	return t

def t_else(t):
	r'si no'
	t.value = 'else'
	return t

def t_while(t):
	r'mientras'
	t.value = 'while'
	return t

def t_for(t):
	r'para cada'
	t.value = 'for'
	return t

def t_in(t):
	r'en'
	t.value = 'in'
	return t

def t_if(t):
	r'si'
	t.value = 'if';
	return t

def t_parena(t):
	r'\('
	return t

def t_parenc(t):
	r'\)'
	return t

def t_opbin(t):
	r'\+|-|\*|/|mod|==|!=|>=|<=|>|<|y|o'
	if t.value == 'mod':
		t.value = '%'
	elif t.value == 'y':
		t.value = 'and'
	elif t.value == 'o':
		t.value = 'or'
	return t

def t_opuna(t):
	r'\+\+|--'
	return t

def t_ask(t):
	r'preguntar'
	t.value = 'input'
	return t

def t_print(t):
	r'imprimir'
	t.value = 'print'
	return t

def t_asig(t):
	r'=|\+=|-=|\*=|/='
	return t

def t_num(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_id(t):
	r'[a-zA-Z_][0-9a-zA-Z_]*'
	return t

def t_proc(t):
	r'proceso'
	t.value = 'def'
	return t

def t_expbool(t):
	r'verdadero|falso'
	if t.value == 'verdadero':
		t.value = 'True'
	else:
		t.value = "False"

	return t

def t_return(t):
	r'retornar'
	t.value = 'return'
	return t

def t_coment(t):
	r'<--'
	t.value = '#'
	return t

def t_tab(t):
	r'(\t)+'
	return t

# Hace el cambio de linea
def t_newline(t):
	r'\n'
	global m_totLineas
	m_totLineas += 1

def t_string(t):	# funciona tanto para comentarios como para strings
	r'[^\n\r]'
	return t

def t_error (t):
    print ("Error lexico")
    t.lexer.skip(1)

# Metodo auxiliar que se encarga de hacer la identacion de cada linea en python
def add_tabs(cantTabs):
	nivel = ""
	for i in cantTabs:	# hace tantos tabs como lo dice el parametro que recibe
		nivel += '\t'
	nivel = '\n'+nivel	# agrega el cambio de linea
	return nivel

import ply.lex as lex
lex.lex()

# parser

# --------------------------------- Producciones ya hechas ---------------------------------
#	* empty
#	* ids o numeros solos (inmediato)
#	* parametro
#	* parametros
#		- puede ser 0, 1 o "n" parametros
#	* tabs
#	* comentarios
#	* operaciones
#		- operaciones aritmeticas
#		- operaciones logicas
#	* pedir cosas al usuario
#	* instruccion: se refiere a una linea de programa y puede tener las siguientes formas
#		- asignacion (tiene operaciones aritmeticas y booleanas)
#		- operaciones unarias
#		- procedimiento
#		- ciclo while
#		- ciclo for
#		- condicionales
# ------------------------------------------------------------------------------------------
def p_root(p):
	'''root : inicio'''
	p[0] = p[1]
	global m_result
	m_result = p[0]
	file = open('output.py', 'w')
	file.write(m_result)
	file.close()

def p_inicio(p):
	'''inicio : instruccion inicio'''
	p[0] = p[1] + p[2]

def p_inicio2(p):
	'''inicio : instruccion '''
	p[0] = p[1]

def p_tabs(p):
	'''tabs : TAB '''
	global m_tabs
	m_tabs = len(str(p[1]))		# cada vez que encuentra un tab incrementa la variable, cada vez que se hace un cambio de linea hay que ponerla en 0 otra vez
	addTabs = add_tabs(m_tabs)
	m_tabs = 0
	p[0] = addTabs

# reconoce epsilon
def p_empty(p):
	'''empty : '''
	p[0] = ''

def p_fin(p):
	'''fininstru : FIN'''
	p[0] = p[1]

# para reconocer tanto numeros solos, ids solos, expresiones booleanas (True/False) solas o strings
def p_inmediato(p):
	'''inmediato : NUM
				 | ID
				 | EXPBOOL'''
	p[0] = p[1]

# reconoce la estructura de un "input" en el pseudocodigo
def p_preguntar(p):
	'''preguntar : tabs ID ASIG ASK PARENA STRING PARENC '''
	p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]

# reconoce tanto operaciones aritmeticas como logicas en el pseudocodigo
def p_operacion(p):
	'''operacion : PARENA operacion PARENC operacion2'''
	p[0] = p[1] + p[2] + p[3] + p[4]

def p_operacion1(p):
	'''operacion : inmediato operacion2'''
	p[0] = p[1]
def p_operacion2(p):
	'''operacion2 : OPBIN operacion operacion3'''
	p[0] = p[1] + p[2] + p[3]

def p_operacion3(p):
	'''operacion3 : operacion2
				  | empty'''
	p[0] = p[1]

# metodo auxiliar para poder factorizar mas facil
def p_opestring(p):
	'''opestring : STRING
				 | operacion '''
	p[0] = p[1]

# reconoce cuando se solicita imprimir algo en consola
def p_imprime(p):
	'''imprime : PRINT PARENA opestring PARENC '''
	p[0] = p[1] + p[2] + p[3] + p[4]

def p_imprimetab(p):
	'''imprimetab : tabs imprime '''
	p[0] = p[1]

# reconoce 2 o mas parametros
def p_parametro(p):
	'''parametro : operacion COMA parametro '''
	p[0] = p[1] + p[2] + ' ' + p[3]

def p_parametro2(p):
	'''parametro : operacion '''
	p[0] = p[1]

# reconoce 0 parametros, 1 parametro o n parametros
def p_parametros(p):
	'''parametros : parametro
				  | empty'''
	p[0] = p[1]

# reconoce comentarios y comentarios identados
def p_comentario(p):
	'''comentario : COMENT STRING '''
	p[0] = p[1] + ' ' + p[2]

def p_comentariotab(p):
	'''comentariotab : tabs comentario '''
	p[0] = p[0] + p[2]

# reconoce la instruccion para retornar de una funcion
# puede retornar operaciones o strings
def p_return(p):
	'''return : RETURN opestring'''
	p[0] = p[1] + p[2]

# estructura general de un procedimiento
def p_procedimiento(p):
	'''procedimiento : PROC ID PARENA parametros PARENC '''
	p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + p[4] +  p[5]

# estructura de una asignacion a una variable
def p_asignacion(p):
	'''asignacion : VAR ID ASIG opestring'''
	p[0] = p[2] + p[3] + p[4]

# estructura de un condicional (if / else)
def p_condicionif(p):
	'''condicionif : IF operacion'''
	p[0] = p[1] + p[2] + ':'

def p_condicionelse(p):
	'''condicionelse : ELSE'''
	p[0] = p[1] + ':'

def p_condicion(p):
	'''condicion : condicionif
				 | condicionelse'''
	p[0] = p[1]

# estructura de un ciclo while
def p_ciclowhile(p):
	'''ciclowhile : WHILE PARENA operacion PARENC'''
	p[0] = p[1] + p[2] + p[3] + p[4] + ':'

# estructura de un ciclo for
def p_ciclofor(p):
	'''ciclofor : FOR ID IN ID'''
	p[0] = p[1] + p[2] + p[3] + p[4] + ':'

# estructura de una operacion unaria
def p_operacionunaria(p):
	'''opeunaria : OPUNA ID '''
	p[0] = p[1] + p[2]

# estructura general de una instruccion que puede ser:
# 	- un procedimiento (metodo / funcion)
# 	- una asignacion
#	- operaciones unarias
# 	- un condicional (if / else)
#	- un ciclo while
# 	- un ciclo for
# ademas acepta instrucciones que estan identadas
def p_instruccion(p):
	''' instruccion : procedimiento
					| asignacion
					| condicion
					| ciclowhile
					| ciclofor
					| opeunaria
					| return'''
	p[0] = p[1]

def p_instrucciontab(p):
	''' instrucciontab : tabs instruccion '''
	p[0] = p[0] + p[2]

def p_error(p):
	global m_totLineas
	global m_reporte
	if p:
		m_reporte +="Error de sintaxis en " + str(p.value) +". En la linea "+str(m_totLineas)
		print(m_reporte)
	else:
		m_reporte += "Error en "+str(m_totLineas)
		print(m_reporte)

import ply.yacc as yacc
yacc.yacc()
# programa

sourceFile = open('prueba.txt', 'r')
for i in archivo:
	yacc.parse(i)
