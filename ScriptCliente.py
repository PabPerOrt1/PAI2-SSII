from socket import *
import sys

IPServidor = "localhost"
puertoServidor = 9899

#se decaran e inicializaran los valores del socket del cliente
socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((IPServidor,puertoServidor))

while True:
    #escribimos el mensaje
    mensaje = input()
    if mensaje != 'adios' :

        #enviamos mensaje
        socketCliente.send(mensaje.encode())
        #recibimos el mensaje
        respuesta = socketCliente.recv(4096).decode()
        print(respuesta)
    else:
        socketCliente.send(mensaje.encode())
        #cerramos socket
        socketCliente.close()
        sys.exit()
