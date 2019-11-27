import random
import re

from libreria.conexion import Conexion

datos = Conexion('localhost', 'fran', 'Hello1234', 'practica_sesiones')


class Ahorcado:
    letras_ok = []
    intentos = 0
    letras_introducidas = []

    def sacar_scores(self, email):
        """
            Coge el email del usuario saca el nombre del usuario y sus puntuaciones de la base de datos.
        """
        query = f'''SELECT u.nombre, e.puntos
        FROM usuarios AS u
        JOIN scores AS e
        ON u.id = e.id_usuario
        WHERE u.email LIKE "%{email}%"'''
        scores = datos.query(query)
        return scores

    def palabra_aleatoria(self):
        """
            Saca una palabra aleatoria de la base de datos, que será la palabra oculta del ahorcado.
        """
        query = f'''SELECT palabra FROM palabaras WHERE activo = 1 ORDER BY RAND() LIMIT 1'''
        palabra = datos.query(query)
        return palabra[0][0]

    def inicio(self, letra_introducida, palabra, ocultar):
        """
            Este método recoje la letra introducida por el usuario en el input, la palabra random que se saca desde el main, y la palabra ya oculta
        """
        ya_introducida = False
        fin = True
        has_ganado = False

        if letra_introducida in self.letras_introducidas:
            ya_introducida = True
        else:
            self.letras_introducidas.append(letra_introducida)
            for i in palabra:
                if i == letra_introducida.upper():
                    self.letras_ok.append(letra_introducida)
                    posicion = re.search(
                        letra_introducida.upper(), palabra).end()
                    ocultar[posicion-1] = letra_introducida
                    # aqui!!!! ya cambia laa _ por la letra correcta jeje
            if letra_introducida.upper() not in palabra:
                self.intentos += 1

        if len(self.letras_ok) == len(palabra):
            has_ganado = False

        # Perder
        if self.intentos == 7:
            fin = False
            self.letras_introducidas = []
            self.letras_ok = []
            self.intentos = 0
        return self.intentos, has_ganado, fin, self.letras_introducidas, ya_introducida, self.letras_ok, self.ocultada
