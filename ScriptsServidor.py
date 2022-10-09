from socket import *

direccionServidor = "localhost"
puertoServidor = 9899

#Generamos un nuevo socket
socketServidor = socket(AF_INET, SOCK_STREAM)
#Establecemos la conexión
socketServidor.bind( (direccionServidor,puertoServidor) )
socketServidor.listen()

while True:
    #Establecemos la conexión
    socketConexion, addr = socketServidor.accept()
    print("Conectando con un cliente", addr)
    while True:
        #recibimos el mensaje del cliente
        mensajeRecibido = socketConexion.recv(4096).decode()
        print(mensajeRecibido)

        #esta condicion no se cumplira hasta que la cadena sea adios
        if mensajeRecibido == 'adios':
            break
        #mandamos mensaje al cliente
        socketConexion.send(input().encode())

    print("Desconectado el cliente", addr)
    #cerramos conexion
    socketConexion.close()