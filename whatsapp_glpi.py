#
# ALTER TABLE glpi_tickets ADD COLUMN processado BOOLEAN DEFAULT FALSE;
#

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import requests
import time

Base = declarative_base()

class Ticket(Base):
    __tablename__ = 'glpi_tickets'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    processado = Column(Boolean, default=False)  
    name = Column(String)
    is_deleted = Column(Boolean)

class Ticket_Users(Base):
    __tablename__ = 'glpi_tickets_users'
    id = Column(Integer, primary_key=True)
    tickets_id = Column(Integer)
    users_id = Column(Integer)
    type = Column(Integer)

class Users(Base):
    __tablename__ = 'glpi_users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = Column(String)

def monitorar_chamados():
    engine = create_engine('mysql+mysqlconnector://root:''@localhost/glpi10')
    Session = sessionmaker(bind=engine)

    #while True:
    try:
        session = Session()

        query_tickets = session.query(Ticket).filter(Ticket.is_deleted==False, Ticket.status==2, Ticket.processado==False).limit(10)

        for ticket in query_tickets:

            requerenteS = ""
            query_requerentes = session.query(Ticket_Users, Users).join(Users, Users.id==Ticket_Users.users_id).filter(Ticket_Users.tickets_id==ticket.id, Ticket_Users.type==1)
            for requerente in query_requerentes:
                requerenteS += requerente.Users.name+" "

            observadoreS = ""
            query_obsv = session.query(Ticket_Users, Users).join(Users, Users.id==Ticket_Users.users_id).filter(Ticket_Users.tickets_id==ticket.id, Ticket_Users.type==3)
            for observador in query_obsv:
                observadoreS += observador.Users.name+" "

            query_designado = session.query(Ticket_Users, Users).join(Users, Users.id==Ticket_Users.users_id).filter(Ticket_Users.tickets_id==ticket.id, Ticket_Users.type==2)
            for designado in query_designado:
                #print("ticket_usersID", designado.Ticket_Users.users_id)
                #print("type", designado.Ticket_Users.type)
                print("Nome", designado.Users.name)
                #print("Requerentes", requerenteS)
                #print("Observadores", observadoreS)

                #Irá fazer a chamada a API

                response = requests.post('https://api.callmebot.com/whatsapp.php', data={
                'chatId': f'{designado.Users.mobile}@c.us',
                'contentType': 'string',
                'content': f'          🔧 *‎ GLPI* 🔧\n\n_Você tem um chamado:_ \n\nNúmero: {ticket.id} \n\n```-``` {ticket.name}\n\n Requerente: {requerenteS}\n\n Observadores: {observadoreS}'
                })

                time.sleep(2)

                if response.status_code == 200:
                    print(f'Chamado processado com sucesso!')
                    ticket.processado = True
                else:
                    print(f'Erro ao processar chamado ')
            
        session.commit()

    finally:
        session.close()

        #print("Verificação concluída. Aguardando 5 minutos.")
        #time.sleep(300)

if __name__ == '__main__':
    monitorar_chamados()
