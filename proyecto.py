# Universidad de Costa Rica
# Escuela de Ciencas de la Computacion e Informatica
# Automatas y Compiladores
# - Fabian Rodriguez
# - Abraham Vega
# I Semestre 2015
# -----------------------------------------------------------
# |		El programa traduce de un pseudocodigo a python		|
# -----------------------------------------------------------

# modulos externos
import ply.lex as lex
import ply.yacc as yacc
import time
# lexer
tokens = ['ID', 'COMA', 'PARENA', 'PARENC', 'OPBIN', 'OPUNA', 'ASIG', 'NUM', 'EXPBOOL', 'COMENT', 'STRING']

reserved = {
	'mientras' : 'WHILE',
	'si_no' : 'ELSE',
	'para cada' : 'FOR',
	'en' : 'IN',
	'si' : 'IF',
	'fin' : 'FIN',
	'var' : 'VAR',
	'procedimiento' : 'PROC',
	'preguntar' : 'ASK',
	'imprimir' : 'PRINT',
	'retornar' : 'RETURN',
	'entonces' : 'ENTONCES'
}
tokens += reserved.values()

m_tabs = 0 	# variable global que lleva cuantos tabs se hicieron en cada linea
m_result = ""
m_totLineas = 1
m_reporte = ""

def t_ID(t):
	r'[_a-zA-Z][_a-zA-Z0-9]*'
	t.type = reserved.get(t.value,'ID')		# busca en la lista de palabras reservadas y si no esta, lo asigna como un ID
	return t

def t_COMA(t):
	r', '
	return t

def t_PARENA(t):
	r'\('
	return t

def t_PARENC(t):
	r'\)'
	return t

def t_OPUNA(t):
	r'\+\+|--'
	return t

def t_ASIG(t):
	r'=|\+=|-=|\*=|/='
	return t

def t_OPBIN(t):
	r'\+|-|\*|/|%|==|!=|>=|<=|>|<|\.y\.|\.o\.'
	if t.value == '.y.':
		t.value = 'and'
	elif t.value == '.o.':
		t.value = 'or'
	return t

def t_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_EXPBOOL(t):
	r'verdadero|falso'
	if t.value == 'verdadero':
		t.value = 'True'
		return t
	else:
		t.value = "False"
		return t

def t_COMENT(t):
	r'\$'
	return t

def t_STRING(t):
	r'\'[a-zA-Z0-9_ ]+\''
	return t

# Hace el cambio de linea
def t_newline(t):
	r'\n'
	global m_totLineas
	m_totLineas += 1

def t_error (t):
    print ("Error lexico")
    t.lexer.skip(1)

#ignora espacios en blanco
t_ignore = " \t"

lex.lex()


# Metodo auxiliar que se encarga de hacer la identacion de cada linea en python
def add_tabs(b):
	global m_tabs
	nivel = ''
	if(b == False):
		nivel = "\n"		# para hacer el cambio de linea despues de la instruccion
	tmp = m_tabs
	while tmp > 0:	# agrega tantos tabs como lo inque m_tabs
		nivel += "\t"
		tmp = tmp -1
	return nivel

# parser

# --------------------------------- Producciones ya hechas ---------------------------------
#	* empty
#	* ids o numeros solos (inmediato)
#	* parametro
#	* parametros
#		- puede ser 0, 1 o "n" parametros
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
	p[0] = str(p[1])
	global m_result
	m_result += '# ---------------------------------------------------------------------\n'
	m_result += '# Programa traducido de pseudocodigo a Python \n'
	m_result += '# por un compilador hecho en el curso de Automatas y Compiladores\n'
	m_result += '# de la Universidad de Costa Rica por los estudiantes:\n'
	m_result += '#	- Fabian Rodriguez Obando\n'
	m_result += '# 	- Abraham Vega Delgado\n'
	m_result += '# Profesor: Luis Quesada\n'
	m_result += '# Fecha de conversion: ' + time.strftime("%x") + '\n'
	m_result += '# ---------------------------------------------------------------------\n'
	m_result += str(p[0])

def p_inicio(p):
	'''inicio : instruccion inicio'''
	p[0] = str(p[1]) + str(p[2])

def p_inicio2(p):
	'''inicio : empty'''
	p[0] = str(p[1])

# reconoce epsilon
def p_empty(p):
	'''empty : '''
	p[0] = ''

def p_fin(p):
	'''fininstru : FIN'''
	global m_tabs
	if m_tabs > 0:
		m_tabs -= 1
	else:
		m_tabs = 0
	p[0] = add_tabs(True) + ''

# para reconocer tanto numeros solos, ids solos, expresiones booleanas (True/False) solas o strings
def p_inmediato(p):
	'''inmediato : NUM
				 | ID
				 | EXPBOOL'''
	p[0] = str(p[1])

# reconoce tanto operaciones aritmeticas como logicas en el pseudocodigo
def p_operacion(p):
	''' operacion : operacion1'''
	p[0] = str(p[1])

def p_operacion_normal_parentesis(p):
	''' operacion1 : operacion OPBIN operacion
				   | PARENA operacion PARENC'''
	p[0] = str(p[1]) + str(p[2]) + str(p[3])

def p_operacion_numero(p):
	''' operacion1 : inmediato'''
	p[0] = str(p[1])

# metodo auxiliar para poder factorizar mas facil
def p_opestring(p):
	'''opestring : STRING
				 | operacion'''
	p[0] = str(p[1])

# reconoce 2 o mas parametros
def p_parametro(p):
	'''parametro : operacion COMA parametro'''
	p[0] = str(p[1]) + ', ' + str(p[3])

def p_parametro2(p):
	'''parametro : operacion'''
	p[0] = str(p[1])

# reconoce 0 parametros, 1 parametro o n parametros
def p_parametros(p):
	'''parametros : parametro
				  | empty'''
	p[0] = str(p[1])

# ---------------------------------------------------------------------------------------
# |		De aqui para abajo son cosas que pueden aparecer en una linea del codigo		|
# ---------------------------------------------------------------------------------------

# reconoce cuando se solicita imprimir algo en consola
def p_imprime(p):
	'''imprime : PRINT PARENA opestring PARENC '''
	p[0] = add_tabs(False) + 'print(' + str(p[3]) + ')'

# reconoce comentarios y comentarios identados
def p_comentario(p):
	'''comentario : COMENT STRING'''
	p[0] = add_tabs(False) + '# ' + str(p[2])

# reconoce la instruccion para retornar de una funcion
# puede retornar operaciones o strings
def p_return(p):
	'''return : RETURN opestring'''
	p[0] = add_tabs(False) + 'return( ' + str(p[2]) + ')'

# estructura general de un procedimiento
def p_procedimiento(p):
	'''procedimiento : PROC ID PARENA parametros PARENC'''
	global m_tabs
	m_tabs = 0
	p[0] = add_tabs(False) + 'def ' + str(p[2]) + '(' + str(p[4]) + '):'
	m_tabs += 1

# estructura de una asignacion a una variable
def p_asignacion(p):
	'''asignacion : VAR ID ASIG opestring'''
	p[0] = add_tabs(False) + str(p[2]) + str(p[3]) + str(p[4])

def p_asignacion_sindeclaracion(p):
	'''asignacion : ID ASIG opestring'''
	p[0] = add_tabs(False) + str(p[1]) + str(p[2]) + str(p[3])

# estructura de un condicional (if / else)
def p_condicionif(p):
	'''condicionif : IF operacion'''
	p[0] = add_tabs(False) + 'if(' + str(p[2]) + '):'
	global m_tabs
	m_tabs += 1
	
def p_condicionelse(p):
	'''condicionelse : ELSE'''
	global m_tabs
	m_tabs -= 1
	p[0] = add_tabs(False) +'else:'
	m_tabs += 1

def p_condicion(p):
	'''condicion : condicionif
				 | condicionelse'''
	p[0] = str(p[1])

# estructura de un ciclo while
def p_ciclowhile(p):
	'''ciclowhile : WHILE PARENA operacion PARENC ENTONCES'''
	p[0] = add_tabs(False) + 'while(' + str(p[3]) + '):'
	global m_tabs
	m_tabs += 1

# estructura de un ciclo for
def p_ciclofor(p):
	'''ciclofor : FOR ID IN ID'''
	p[0] = add_tabs(False) + 'for ' + str(p[2]) + ' in ' + str(p[4]) +':'
	global m_tabs
	m_tabs += 1

# estructura de una operacion unaria
def p_operacionunaria(p):
	'''opeunaria : OPUNA ID '''
	p[0] = add_tabs(False) + str(p[1]) + str(p[2])

# reconoce la estructura de un "input" en el pseudocodigo
def p_preguntar(p):
	'''preguntar : VAR ID ASIG ASK PARENA STRING PARENC '''
	p[0] = add_tabs(False) + str(p[2]) + ' = input(' + str(p[6]) +')'

def p_preguntar2(p):
	'''preguntar : ID ASIG ASK PARENA STRING PARENC'''
	p[0] = add_tabs(False) + str(p[1]) + " = input(" + str(p[5]) + ')'

def p_llamado(p):
	'''llamado : ID PARENA parametros PARENC'''
	p[0] = add_tabs(False) + str(p[1]) + '(' + str(p[3]) + ')'
# estructura general de una linea de programa que puede ser:
# 	- un procedimiento (metodo / funcion)
# 	- una asignacion
#	- operaciones unarias
# 	- un condicional (if / else)
#	- un ciclo while
# 	- un ciclo for
#	- un comentario
#	- imprimir
#	- preguntar al usuario
# ademas acepta instrucciones que estan identadas
def p_instruccion(p):
	''' instruccion : procedimiento
					| asignacion
					| condicion
					| ciclowhile
					| ciclofor
					| opeunaria
					| return
					| comentario
					| imprime
					| preguntar
					| fininstru
					| llamado'''
	global m_tabs
	p[0] = str(p[1])

def p_error(p):
	global m_totLineas
	global m_reporte
	if p:
		m_reporte +="Error de sintaxis en " + str(p.value) + ". En la linea " + str(m_totLineas)+'\n'
		print(m_reporte)
	else:
		m_reporte += "Error en "+str(m_totLineas)+'\n'
		print(m_reporte)

yacc.yacc()
# programa

sfname = ""
sfname = str(raw_input('Ingrese el nombre del archivo que desea convertir a python> '))
sourceFile = open(sfname, 'r')
pseudo = ""
for line in sourceFile:
	pseudo += str(line)
yacc.parse(pseudo)
sfname = str(raw_input('Ingrese el nombre con el que quiere guardar el archivo> '))
file = open(sfname+".py", 'w')
file.write(m_result)
file.close()
sourceFile.close()
