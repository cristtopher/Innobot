#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Skype4Py
import random
import logging
import sqlite3
import smtplib
from email.mime.text import MIMEText
# import base64
# from Examples.EchoClient import WhatsappEchoClient 


def commands(Message, Status):
    if Status == 'SENT' or (Status == 'RECEIVED'): 
        heuristic(Message.Id, Message.FromHandle, Message.Body, Message.Datetime)
        logging.info(Message.Body)
        if Message.Body == "!?":
            alive(Message)
        elif "!ip" in Message.Body:
            searchip(Message)
        elif "!ping" in Message.Body:
            ping(Message)
        elif "buenos dias" in Message.Body:
            greet(Message)
        elif "hola" in Message.Body:
            greet()
        else:
            pass
    else:
        pass


def alive(Message):
    Message.Chat.Sendsendwhatapp()
    print "Ping Command Received \n"


def ping(Message):
    Message.Chat.SendMessage('Centro Online')
    print "Ping Command Received \n"


def greet():
    #Message.Chat.SendMessage('Hola buenas, Cristtopher por aca, Jefe Soporte Tecnico')
    Message.Chat.SendMessage('Hola, que tal')
    #Message.Chat.SendMessage('en que te puedo ayudar?')
    print "Greeting Received!.\n"
    sendwhatapp('Greeting Received!.')
    


def cmd_dice(Message):
    Message.Chat.SendMessage('Robot: Put a bet on numbers 1 through 6.')
    time.sleep(8)
    answer = random.randint(1,6)
    Message.Chat.SendMessage('Robot: *rolls dice*')
    time.sleep(1)
    Message.Chat.SendMessage('Robot: The dice rolled the number:')
    Message.Chat.SendMessage(answer)
    print "Someone's playing dice. \n"


def heuristic(Id, User, Message, Date):
    try:
        if User != 'cristtopher_quintana':
            sendmail(User, Message)
            sendwhatapp(Message)
            connection = sqlite3.connect(Path + 'memory.db')
            cursor = connection.cursor()
            cursor.execute("insert into messages(id, user, body, date) values (%i,'%s','%s','%s')" % (Id, User, Message, Date))
            connection.commit()
            connection.close()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
        logging.error(e.args[0])


def searchip(Message):
    print "IP Command Received \n"
    Message.Chat.SendMessage('la ip es: ')


def sendmail(User, Message):
    # Creamos el mensaje
    text = User + ' -> ' +  Message
    msg = MIMEText(text)
    msg['Subject'] = 'Skype'
    msg['From'] = 'cquintana@innovex.cl'
    msg['To'] = 'cquintana@innovex.cl'
    mailServer = smtplib.SMTP('smtp.1und1.de',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login("cquintana@innovex.cl","xxxx")
    mailServer.sendmail("cquintana@innovex.cl", "cquintana@innovex.cl", msg.as_string())
    mailServer.close()


def sendwhatapp(Message):
    password = "cpL+ocV0i+V65/L0uO/7pR9XJLU="                      #Password dada al registrar el numero.
    password = base64.b64decode(bytes(password.encode('utf-8')))   #Codificacion de Password para envio a los servidores de whatsApp.
    username = '56962365854'                                       #Numero de telefono para el inicio de secion.
    keepAlive= False                                               #Conexion persistente con el servidor.
    #......................................................................
    whats = WhatsappEchoClient("+56962365854", Message, keepAlive)     #Inicia el cliente para el envio de mensajes por WhatsApp.
    whats.login(username, password)  


print "|----------------------------------------------|\n";
print "|               Welcome To InnoBot             |\n";
print "|----------------------------------------------|\n";
skype = Skype4Py.Skype(); 
skype.OnMessageStatus = commands 

if skype.Client.IsRunning == False: 
    skype.Client.Start() 
skype.Attach();
Path = '/home/cristtopher/.Skype/'
print 'InnoBot currently running on user',skype.CurrentUserHandle, "\n"
logging.basicConfig(filename=Path + 'Skype.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.info('Started')
while True: 
    raw_input('')
