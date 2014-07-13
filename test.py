#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from Examples.EchoClient import WhatsappEchoClient             #Importa la Clace WhatsappEchoClient, dedicada a envio de mensajes.
#................Clave de Acceso a WhatsApp............................
password = "xhB7OCqb2tFPR1dBBsE+pCQoECM="                      #Password dada al registrar el numero.
password = base64.b64decode(bytes(password.encode('utf-8')))   #Codificacion de Password para envio a los servidores de whatsApp.
username = '56978783158'                                     #Numero de telefono para el inicio de secion.
keepAlive= False                                               #Conexion persistente con el servidor.
#......................................................................
nombre = "nombre"
mensaje = "mensaje"
Text = "%s, %s" %(nombre, mensaje)
whats = WhatsappEchoClient("56962365854", Text, keepAlive)     #Inicia el cliente para el envio de mensajes por WhatsApp.
whats.login(username, password)  