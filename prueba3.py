# ---------------------------------------------------------------------
# Programa traducido de pseudocodigo a Python 
# por un compilador hecho en el curso de Automatas y Compiladores
# de la Universidad de Costa Rica por los estudiantes:
#	- Fabian Rodriguez Obando
# 	- Abraham Vega Delgado
# Profesor: Luis Quesada
# Fecha de conversion: 07/09/15
# ---------------------------------------------------------------------

def multiplicar(x, y):
	return(x*y)
# 'Funcion que hace un ciclo'
def cicloSumador(inicio):
	count = inicio
	respuesta = 0
	while(count!=0):
		respuesta += suma(count, count+3)
		count -= 1	
	return(respuesta)
def main():
	dato = input('Ingrese desde donde quiere empezar el ciclo ')
	respuesta = 0
	respuesta = cicloSumador(dato)
	print('El resultado final es')
	print(respuesta)
	respuesta = str(dato+2)