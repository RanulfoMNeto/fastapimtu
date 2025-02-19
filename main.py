from automata.tm.dtm import DTM
from fastapi import FastAPI, Request, Depends
from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import engine, SessionLocal
from util.email_body import EmailSchema
from prometheus_fastapi_instrumentator import Instrumentator
from pika import ConnectionParameters, PlainCredentials, BlockingConnection,BasicProperties
from typing import List
from pydantic import BaseModel
import json

class RabbitMQPublisher:
    def __init__(self) -> None:
        self._host = "rabbitMQ"
        self._port = 5672
        self._username = "guest"
        self._password = "guest"
        self._exchange = "data_exchange"
        self._routing_key = ""
        self._channel = self._create_channel()
    
    def _create_channel(self):
        connection_parameters = ConnectionParameters(
            host=self._host,
            port=self._port,
            credentials=PlainCredentials(
                username=self._username,
                password=self._password
            )
        )
        channel = BlockingConnection(connection_parameters).channel()
        return channel

    def send_message(self, body):
        self._channel.basic_publish(
            exchange = self._exchange,
            routing_key = self._routing_key,
            body = json.dumps(body),
            properties = BasicProperties(
                delivery_mode = 2
            )
        )


class RabbitMQConsumer:
    def __init__(self) -> None:
        self.__host = "rabbitMQ"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "data_queue"
        self.__channel = self.__create_channel()
        self.__conf = ConnectionConfig(
            MAIL_USERNAME="afe5541c767792",
            MAIL_PASSWORD="23f22a602b46f6",
            MAIL_FROM="from@example.com",
            MAIL_PORT=587,
            MAIL_SERVER="sandbox.smtp.mailtrap.io",
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )

    def __create_channel(self):
        connection_parameters = ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )
        channel = BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )

        return channel

    async def simple_send(self, email: EmailSchema, result: str, configuration: str):
        html = """
        <p>Thanks for using Fastapi-mail</p>
        <p> The result is: """ + result + """</p>
        <p> We have used this configuration: """ + configuration + """</p>
        """
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=email.dict().get("email"),
            body=html,
            subtype=MessageType.html)

        fm = FastMail(self.__conf)
        await fm.send_message(message)
        return "OK"

    async def consumeQueue(self):
        while True:
            method, properties, body = self.__channel.basic_get(
                queue=self.__queue,
                auto_ack=True
            )

            if(body != None):
                data = json.loads(body.decode())
                
                await self.simple_send(
                    EmailSchema(email=["to@example.com"]),
                    result=data["msg"],
                    configuration=str(data["info"])
                )
                
            if not method:
                break

# Modelo de imput
class MaquinaTuring(BaseModel):
    states: List[str]
    input_symbols: List[str]
    tape_symbols: List[str]
    initial_state: str
    blank_symbol: str
    final_states: List[str]
    transitions: dict
    input: str

# Conectando ao rabbitMQ
connection_parameters = ConnectionParameters(
    host="rabbitMQ",
    port=5672,
    credentials= PlainCredentials(
        username="guest",
        password="guest"
    )
)

# Configuração de email
conf = ConnectionConfig(
    MAIL_USERNAME="b6d1b9dff6dedc",
    MAIL_PASSWORD="5dd837e444b86a",
    MAIL_FROM="from@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

app = FastAPI()

Instrumentator().instrument(app).expose(app)

models.Base.metadata.create_all(bind=engine)

rabbitMQPublisher = RabbitMQPublisher()

rabbitmqConsumer = RabbitMQConsumer()

# Patter Singleton
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get_history/{id}")
async def get_history(id: int, db: Session = Depends(get_db)):
    history = crud.get_history(db=db, id=id)
    if history is None:
        return {
            "code": "404",
            "msg": "not found"
        }
    return history


@app.get("/get_all_history")
async def get_all_history(db: Session = Depends(get_db)):
    history = crud.get_all_history(db=db)
    return history

@app.get("/")
async def dtm2(info: Request):
    print("Rodando")
    return {"code": "200"}


@app.post("/dtm")
async def dtm(listTuringMachinne: List[MaquinaTuring], db: Session = Depends(get_db)):
    for it in listTuringMachinne:
        states = set(it.states)
        if len(states) == 0:
            return {
                "code": "400",
                "msg": "states cannot be empty"
            }

        input_symbols = set(it.input_symbols)
        if len(input_symbols) == 0:
            return {
                "code": "400",
                "msg": "input_symbols cannot be empty"
            }
        
        tape_symbols = set(it.tape_symbols)
        if len(tape_symbols) == 0:
            return {
                "code": "400",
                "msg": "tape_symbols cannot be empty"
            }

        initial_state = it.initial_state
        if initial_state == "":
            return {
                "code": "400",
                "msg": "initial_state cannot be empty"
            }
        
        blank_symbol = it.blank_symbol
        if blank_symbol == "":
            return {
                "code": "400",
                "msg": "blank_symbol cannot be empty"
            }
        
        final_states = set(it.final_states)
        if len(final_states) == 0:
            return {
                "code": "400",
                "msg": "final_states cannot"
            }
        
        transitions = it.transitions
        if len(transitions) == 0:
            return {
                "code": "400",
                "msg": "transitions cannot be empty"
            }

        input = it.input
        if input == "":
            return {
                "code": "400",
                "msg": "input cannot be empty"
            }

        dtm = DTM (
            states=states,
            input_symbols=input_symbols,
            tape_symbols=tape_symbols,
            transitions=transitions,
            initial_state=initial_state,
            blank_symbol=blank_symbol,
            final_states=final_states,
        )

        if dtm.accepts_input(input):
            print('accepted')
            mensagem = {
                "code": "200",
                "msg": "accepted",
                "info": {
                    "states": list(states),
                    "input_symbols": list(input_symbols),
                    "tape_symbols": list(tape_symbols),
                    "initial_state": initial_state,
                    "blank_symbol": blank_symbol,
                    "final_states": list(final_states),
                    "transitions": transitions,
                    "input": input
                }
            }
        else:
            print('rejected')
            mensagem = {
                "code": "400",
                "msg": "rejected",
                "info": {
                    "states": list(states),
                    "input_symbols": list(input_symbols),
                    "tape_symbols": list(tape_symbols),
                    "initial_state": initial_state,
                    "blank_symbol": blank_symbol,
                    "final_states": list(final_states),
                    "transitions": transitions,
                    "input": input
                }
            }
            print(mensagem)

        rabbitMQPublisher.send_message(mensagem)

        history = schemas.History(query=str(mensagem["info"]), result=mensagem["msg"])
        crud.create_history(db=db, history=history)

    await rabbitmqConsumer.consumeQueue()
    return "finished"