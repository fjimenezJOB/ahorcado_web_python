import pymysql

class Conexion():
    def __init__(self, host, usuario, contraseña, basedatos):
        self.conexion = pymysql.connect(
            host=host, user=usuario, password=contraseña, db=basedatos)

    def query(self, sql):
        with self.conexion.cursor() as cursor:
            cursor.execute(sql)
            self.conexion.commit()
            return cursor.fetchall()

    def cerrar_bd(self):
        self.conexion.close()