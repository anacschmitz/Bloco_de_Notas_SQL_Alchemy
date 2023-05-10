from Infra.configs.connection import DBConnectionHandler
from Infra.entities.nota import Nota

class NotaRepository:

    # Método para consultar as notas no banco
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

    def select(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).filter(Nota.id == id).first()
            return data

    # Método para inserir nota no banco
    def insert(self, nota):
        with DBConnectionHandler() as db:
            try:
                db.session.add(nota)
                db.session.commit()
                return 'ok'
            except Exception as e:
                db.session.rollback()
                return e

    def delete(self, id):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == id).delete()
            db.session.commit()

    def update(self, nota:Nota):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id == nota.id).update({'titulo_nota' : nota.titulo_nota, 'texto' : nota.texto})
            db.session.commit()
