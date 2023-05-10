from Infra.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime


class Nota(Base):
    __tablename__ = 'nota'

    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo_nota = Column(String(20), nullable=False)
    texto = Column(String(100), nullable=False)
    data = Column(DateTime)

    def __repr__(self):
        return f'Título da nota = {self.titulo_nota}, id = {self.id}'
