import random
import re

from libreria.conexion import Conexion

datos = Conexion('localhost', 'fran', 'Hello1234', 'practica_sesiones')


class Ahorcado:
   
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

    def inicio(self):
        """
            Este método recoje la letra introducida por el usuario en el input, la palabra random que se saca desde el main, y la palabra ya oculta
        """
        pass
