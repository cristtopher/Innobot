#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import Skype4Py
import random
import logging
import sqlite3
import base64
from Examples.EchoClient import WhatsappEchoClient 


def commands(Message, Status):
    exist = False
    #if Status == 'SENT' or Status == 'RECEIVED':
    if Status == 'RECEIVED':
        memory = sqlite3.connect(Path + 'memory.db')
        cursor = memory.cursor()
        cursor.execute("SELECT name FROM messages")
        for row in cursor:
            if row[0] == Message.ChatName:
                exist = True
            else:
                exist = False
        if exist == False:
            cursor.execute("insert into messages values ('%s','%s','%s','%s')" % (Message.ChatName, Message.FromHandle, Message.Body, Message.Datetime))
            memory.commit()
            knowledge(Message.ChatName, Message.FromHandle, Message.Body, Message.Datetime)
            sendwhatapp(Message.FromHandle, Message.Body)
            logging.info(Message.Body)
            if "ola" in Message.Body:
                greet(Message)
            elif "uenas" in Message.Body:
                greet(Message)
            else:
                pass
        else:
            exist = False
        memory.close()
    else:
        pass


def greet(Message):
    time.sleep(3) #more human
    if time.strftime("%p") == "AM":
        timeis = "buen día"
    else:
        timeis = "buenas tardes"
    responses1 = {1: "Hola %s" % (timeis), 
                2: timeis,
                3: "que tal",
                4: "Hola",
                5: "Hola estimado",
                6: "Hola como te va?"}
    responses2 = {1: "¿en qué te puedo ayudar?", 
                2: "cuentame, como te ayudo?",
                3: "como te ayudo?",
                4: "dime, en que te puedo ayudar?",
                5: "dime, como te ayudo?",
                6: "cuentame"}
    response = random.randrange(1, 6)
    Message.Chat.SendMessage(responses1[response])
    time.sleep(2) #more human
    Message.Chat.SendMessage(responses2[response])
    print "Greeting Received from %s!.\n" % (Message.FromHandle)


def heuristic():
    # retomar despues de unos meses para que base de conocimientos se llene
    pass
    

def knowledge(Name, User, Message, Date):
    try:
        exist = False
        connection = sqlite3.connect(Path + 'knowledge.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name, body FROM messages")
        for row in cursor:
            if row[0] == Name and row[1] == Message:
                exist = True
            else:
                exist = False
        if exist is False:
            cursor.execute("insert into messages values ('%s','%s','%s','%s')" % (Name, User, Message, Date))
            print "Message remembered in knowledge"
            logging.info("Message remembered in knowledge")
            connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
        logging.error(e.args[0])


def sendwhatapp(User, Message):
    password = "xhB7OCqb2tFPR1dBBsE+pCQoECM="                      #Password dada al registrar el numero.
    password = base64.b64decode(bytes(password.encode('utf-8')))   #Codificacion de Password para envio a los servidores de whatsApp.
    username = '56978783158'                                       #Numero de telefono para el inicio de secion.
    keepAlive= False          
    Text = "%s -> %s" %(str(User), str(Message))                            #Conexion persistente con el servidor.
    whats = WhatsappEchoClient("56962365854", Text, keepAlive)     #Inicia el cliente para el envio de mensajes por WhatsApp.
    whats2 = WhatsappEchoClient("56951892025", Text, keepAlive)     #Inicia el cliente para el envio de mensajes por WhatsApp.
    print "Message sent to whatsApp"
    logging.info("Message sent to whatsApp")
    whats.login(username, password)
    whats2.login(username, password)

if __name__ == "__main__":
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = commands
    if skype.Client.IsRunning == False:
        skype.Client.Start()
    skype.Attach();
    Path = '/home/cristtopher/.Skype/'
    print 'This Bot currently running on user', skype.CurrentUser.FullName,\
     "(" + skype.CurrentUserHandle + ")", "\n"
    logging.basicConfig(filename=Path + 'Skype.log',level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logging.info('Started')
    while True:
        raw_input('')
