import sqlite3
from PyQt5 import QtSql, QtWidgets


class Connection:
    def create_db(filename):
        # función que crea la base de datos si esta no existe previamente
        try:
            connection = sqlite3.connect(database=filename)
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS scores (id INTEGER NOT NULL, '
                        'score INTEGER NOT NULL, PRIMARY KEY (id AUTOINCREMENT))')
            connection.commit()
        except Exception as error:
            print('La base de datos no ha sido creada.', error)

    def db_connect(filedb):
        # función que conecta el juego a la base de datos
        try:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None,
                                               "No es posible abrir la base de datos.\n Haz clic para continuar",
                                               QtWidgets.QMessageBox.Cancel)
                return False
            else:
                print("Conexión establecida.")
                return True
        except Exception as error:
            print('Error en el módulo de la conexión.', error)

    def saveScore(score):
        # función que guarda la puntuación de la partida en la base de datos
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into scores (score) VALUES (:score)')
            query.bindValue(':score', score)

            if query.exec_():
                print('Puntuación guardada.')
            else:
                print('Puntuación no guardada.')

        except Exception as error:
            print('Error en el módulo de guardar la puntuación.', error)

    def maxScore():
        # función que coge la puntuación máxima de la base de datos y la retorna como output
        try:
            scores = []
            query = QtSql.QSqlQuery()
            query.prepare('SELECT MAX(score) FROM scores')

            if query.exec_():
                while query.next():
                    scores.append(query.value(0))
                max_score = str(scores[0])
                return max_score
            else:
                print(scores)

        except Exception as error:
            print('Error en el módulo de máxima puntuación.', error)
