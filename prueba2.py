# ---------------------------------------------------------------------
# Programa traducido de pseudocodigo a Python 
# por un compilador hecho en el curso de Automatas y Compiladores
# de la Universidad de Costa Rica por los estudiantes:
#	- Fabian Rodriguez Obando
# 	- Abraham Vega Delgado
# Profesor: Luis Quesada
# Fecha de conversion: 07/08/15
# ---------------------------------------------------------------------

def sumador(a, b):
	tmp1=a+1
	tmp2=b+3
	result=0
	# 'Esa variable va a retornarse'
	while(tmp1>=1):
		if(b!=0):
			result+=(tmp1+tmp2)-(a/b)
		else:
			print('El valor de b no es admitido ya que es un cero')			
	print(result)
def main():
	num1 = input('Ingrese el primer numero ')
	num2 = input('Ingrese el segundo numero ')
	sumador(num1, num2)