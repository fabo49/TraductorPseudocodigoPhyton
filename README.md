# Traductor de pseudocódigo a código Phyton
### Información

El programa recibe un codigo en pseudocodigo en un archivo .txt y lo traduce a codigo Python.

Se utilizo PLY como parser, puede encontrar mas detalles de PLY [aqui](http://www.dabeaz.com/ply/).

* Este traductor cumple con dos objetivos principales:
    1. Que el usuario aprenda la lógica necesaria para desarrollar programas sencillos, sin el inconveniente de lidear con una sintaxis complicada, lo que es ideal para principiantes.
    2. Una vez que escribe su código, la persona puede revisar el código generado en Python y de esta forma comprender como funciona ese lenguaje de programación.

### Manual de usuario

Básicamente se corre el programa **Python** llamado *proyecto.py* y el programa le va a solicitar al usuario que ingrese el nombre del archivo en formato .txt donde se encuentra el pseudocódigo que quiere pasar a Python, no es necesario indicar *.txt*, con solo el nombre del archivo es suficiente.

**Este archivo tiene que encontrarse en la misma carpeta desde la que se está corriendo el programa o de lo contrario el usuario va a tener que ingresar la!ruta completa hacia el archivo.**

Si el programa encontró  algún error con el archivo de entrada, le va a indicar al usuario del error y va a terminar la ejecución. En caso contrario, el programa le va a solicitar el nombre con el que quiere que guarde el archivo de salida en formato .py. **El programa pone la terminación .py automática, por lo que no es necesario que el usuario la ingrese.**

### Ejemplo de traducción

* Pseudocodigo:
  ```
  procedimiento sumador(a, b)
    var tmp1 = a+1
    var tmp2 = b+3
    var result = 0
    $'Esa variable va a retornarse'
    mientras(tmp1 >= 1) entonces
      si b != 0
        result += (tmp1+tmp2)-(a/b)
      si_no
        imprimir('El valor de b no es admitido ya que es un cero')
      fin
    fin
    imprimir(result)
  fin
  
  procedimiento main()
    var num1 = preguntar('Ingrese el primer numero ')
    var num2 = preguntar('Ingrese el segundo numero ')
    sumador(num1, num2)
  fin
  ```

* Código traducido:
  ```python
  # ---------------------------------------------------------------------
  # Programa traducido de pseudocodigo a Python 
  # por un compilador hecho en el curso de Automatas y Compiladores
  # de la Universidad de Costa Rica por los estudiantes:
  #	- Fabian Rodriguez Obando
  # - Abraham Vega Delgado
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
  	```
---
### Autores
* Fabián Rodríguez Obando [GitHub](https://github.com/fabo49)
* Abraham Vega Delgado
