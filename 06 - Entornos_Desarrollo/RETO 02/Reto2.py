# Alumno: Francisco José García Franco
# Asignatura: Entornos de Desarrollo
# Módulo: 1º DAM UAX
# Archivo: Reto2.py

# Definición de la clase
class Personaje:

    # Constructor con atributos nombre, peso, altura
    def __init__(self,nombre,peso,altura):
        self.nombre = nombre    # String
        self.peso = peso        # int
        self.altura = altura    # int
        self.energia = 100      # int

        # Información por pantalla
        print(f"Se ha creado el personaje {self.nombre} con peso {self.peso} y altura {self.altura}")
        print(f"El nivel de energía de {self.nombre} es de {self.energia}/100\n")

    # Método de reducción de energía por daño
    def recibirDanio(self,danio):

        self.energia -= danio
        print(f"{self.nombre} ha recibido un daño")

        if self.energia <= 0:
            print(f"¡¡¡DAÑO FATAL!!!: {self.nombre} ha sido derrotado\n")
            exit()  # Sale del programa
        else:
            print(f"El nivel de energía de {self.nombre} es de {self.energia}/100\n")

    # Método de recarga de energía
    def recargarEnergia(self,incremento):

        self.energia += incremento
        print(f"{self.nombre} ha recargado su nivel de energía")

        if self.energia >100:
            self.energia = 100
        print(f"El nivel de energía de {self.nombre} es de {self.energia}/100\n")

if __name__ == "__main__":

    print("CREACIÓN Y TRATAMIENTO DE ENERGÍA DE PERSONAJE")
    print("##############################################\n")

    # Creación de personaje
    personaje1 = Personaje("Vladimir",78,180)

    # Simulación de pérdida de energía y recarga
    personaje1.recibirDanio(10)
    personaje1.recargarEnergia(15)

    # Simulación de derrota del personaje
    personaje1.recibirDanio(150)
