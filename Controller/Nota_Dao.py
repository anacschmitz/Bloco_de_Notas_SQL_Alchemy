import sqlite3

from Model.Nota import Nota


class DataBase:
    def __init__(self, nome='system.db'):
        self.connection = None
        self.name = nome

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(e)

    def create_table_notas(self):
        self.connect()
        cursor = self.connection.cursor()
        query = """
           CREATE TABLE IF NOT EXISTS BLOCO (
           ID INTEGER PRIMARY KEY AUTOINCREMENT,
           TITULO_NOTA TEXT (25),
           TEXTO TEXT,
           DATA DATE
           )
           """
        cursor.execute(query)
        self.close_connection()

    def salvar_nota(self, nota: Nota):
        titulo = nota.titulo_nota
        data = nota.data
        texto = nota.texto

        self.connect()
        cursor = self.connection.cursor()
        query = "INSERT INTO BLOCO ('TITULO_NOTA', 'TEXTO', 'DATA') VALUES (?, ?, ?)"""

        try:
            cursor.execute(query, (titulo, texto, data))
            self.connection.commit()
            return 'ok'
        except sqlite3.Error as e:
            return e

    def consultar_nota(self, id:int):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""SELECT id, TITULO_NOTA, TEXTO, DATA FROM BLOCO WHERE ID = '{id}' """)
            return cursor.fetchone()
        except sqlite3.Error as e:
            return None
        finally:
            self.close_connection()

    def deletar_nota(self, id):
        self.connect()
        try:
            cursor = self.connection.cursor()
            id_inteiro = int(id)
            cursor.execute("DELETE FROM BLOCO WHERE ID = ?", (id_inteiro,))
            self.connection.commit()
            return 'ok'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()

    def atualizar_nota(self, nota=Nota):
        self.connect()
        print(nota.__dict__)
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""UPDATE BLOCO SET TITULO_NOTA = '{nota.titulo_nota}', TEXTO = '{nota.texto}' 
            WHERE ID = '{nota.id}'""")
            self.connection.commit()
            return 'ok'
        except sqlite3.Error as e:
            print(e)
        finally:
            self.close_connection()

    def consultar_bloco(self):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""SELECT * FROM BLOCO""")
            bloco_de_notas = cursor.fetchall()
            return bloco_de_notas
        except:
            return None
        finally:
            self.close_connection()
