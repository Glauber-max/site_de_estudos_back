from app.database.conecction import Base, db
from app.models.agenda import Agenda
from app.models.resumo import Resumo
from app.models.questoes import Questao
from app.models.usuario import Usuario
from app.models.anotacoes import Anotacoes

def criar_table():
    print("criando table")
    Base.metadata.create_all(db)
    print("table criado com sucesso")

if __name__ == "__main__":
    criar_table()