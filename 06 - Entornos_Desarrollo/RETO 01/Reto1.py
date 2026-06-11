# Alumno: Francisco José García Franco
# Asignatura: Entornos de Desarrollo
# Módulo: 1º DAM UAX
# Archivo: Reto1.py

# Importación de la librería random
import random

def adivina_operacion():

    # Petición de entrada de datos al usuario
    print("--Introduzca dos números para realizar una operación--")
    print("------------------------------------------------------")
    # Llamada a una función de validación de formato de datos
    num1 = solicitar_entrada_valida("Primer número: ")
    num2 = solicitar_entrada_valida("Segundo número: ")

    #Elección aleatoria de la operación
    operacion_valida = False    #Variable de control para excepciones (división por 0)

    while not operacion_valida:
        operacion = random.randint(1,4) #1 = suma, 2 = resta, 3 = multiplicación, 4 = división
        operacion_valida = True

        # Si la operación es dividir por 0 no es válida
        if operacion == 4 and num2 == 0:
            operacion_valida = False

    # Cálculo de la operación
    # Se redondean los cálculos a dos decimales
    if operacion == 1:
        resultado = round(num1 + num2, 2)
        nombre_operacion = "suma"
        simbolo = "+"
    elif operacion == 2:
        resultado = round(num1 - num2, 2)
        nombre_operacion = "resta"
        simbolo = "-"
    elif operacion == 3:
        resultado = round(num1 * num2, 2)
        nombre_operacion = "multiplicación"
        simbolo = "x"
    elif operacion == 4:
        # Redondeamos a 2 decimales para facilitar la adivinanza
        resultado = round(num1 / num2, 2)
        nombre_operacion = "división"
        simbolo = "/"

    print(f"\nSe ha realizado una {nombre_operacion} ({simbolo}) con tus números.\n")

    print("(Nota: Si el resultado tiene decimales, redondea la respuesta con máximo 2 decimales)")

    #Bucle de adivinanza
    intentos = 0
    while True:
        try:
            solucion_propuesta = round(float(input("\n¿Cuál es el resultado?: ")),2)
            intentos += 1

            if solucion_propuesta == resultado:
                print(f"¡Correcto! El resultado de {num1} {simbolo} {num2} es {resultado}.")
                print(f"Número de intentos: {intentos}")
                break
            elif solucion_propuesta > resultado:
                print("Pista: Tu respuesta es mayor que el resultado real.")
            else:
                print("Pista: Tu respuesta es menor que el resultado real.")

        except ValueError:
            print("El formato introducido no es válido. Introduce un número válido.")


#Función de validación del formato de la entrada
def solicitar_entrada_valida(peticion):

    # Bucle mientras no se introduce dato válido
    while True:
        try:
            return float(input(peticion))   # return rompe el bucle
        except ValueError:
            print("Formato no válido. Introduzca un número")

if __name__ == "__main__":

    print(f"\nADIVINA EL RESULTADO")
    print(f"####################\n")
    adivina_operacion()

