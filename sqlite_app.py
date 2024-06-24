from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String 
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy import join
from sqlalchemy import select

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer,primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String)

    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, Nome={self.nome}, CPF={self.cpf}, endereco={self.endereco})"

class Conta(Base):
    __tablename__ = "conta"

    id = Column(Integer,primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    numero = Column(Integer)
    saldo = Column(Float)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo},agencia = {self.agencia}, numero = {self.numero}, saldo = {self.saldo})"

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)


with Session(engine) as session:
    honda = Cliente(
        nome='Mitsuo Honda',
        cpf='123456789',
        endereco='Rua do Balacubaco, 666',
        conta = [Conta(tipo='Conta Corrente',agencia='001',numero=1,saldo=1000)]
    )

    fernanda = Cliente(
        nome='Fernanda e Sorocabo',
        cpf='987654321',
        endereco='Rua de Madrid, 16',
        conta = [Conta(tipo='Conta Corrente',agencia='001',numero=2,saldo=1000)]
    )

    #Enviando objetos para o banco de Dados (persiste)
    session.add_all([honda,fernanda])

    session.commit()
    print("Commit Realizado com Sucesso!")

print("")

cpf_procurado = input("CPF: ")

with Session(engine) as Session:
    stmt = session.query(Cliente,Conta).join(Conta,Cliente.id ==Conta.cliente_id).filter(Cliente.cpf==cpf_procurado)

    resultados = stmt.all()

    if resultados:
        for cliente,conta in resultados:
            print(f"Cliente: {cliente}, Conta: {conta}")
    else:
        print("CPF não encontrado!")