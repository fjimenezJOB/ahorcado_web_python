import random
import re
from flask import session

from libreria.conexion import Conexion

datos = Conexion('localhost', 'fran', 'Hello1234', 'practica_sesiones')


class Ahorcado:
    vidas = 8
    escondida = []
    erroneas = []
    letras = []
    fin = False

    def scores(self, email):
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

    def inicio(self,palabra, letra ):
        """
            Este método recoje la letra introducida por el usuario en el input, la palabra random que se saca desde el main, y la palabra ya oculta
        """
        error = False

        if session['inicio'] == True:
            for i in range(len(palabra)):
                self.escondida.append('_')
            session['inicio'] = False

        if letra not in self.letras:
            for i in range(len(palabra)):
                if palabra[i] not in self.letras:
                    if palabra[i] == letra:
                        self.escondida[i] = letra
                        self.letras.append(letra)
                        
            if letra not in self.letras:
                self.vidas -= 1
                self.erroneas.append(letra)
            else:
                self.letras.append(letra)
        else:
            error = True

        if self.vidas <= 0:
            self.fin = True
            self.vidas = 8
            session['inicio'] = True
            self.escondida = []
            self.erroneas = []
            self.letras = []

        session['escondida'] = self.escondida
        session['vidas'] = self.vidas
        session['erroneas'] = self.erroneas
        session['fin'] = self.fin
        session['yaIntroducida'] = error
        session['todas_letras'] = self.letras
