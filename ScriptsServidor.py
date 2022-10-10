from socket import *
import hmac

#Serv siempre conectao o no
#Hacer bien nonce
#log

direccionServidor = "localhost"
puertoServidor = 9899
nonceServ=1

with open("Config.config") as configfile:
        linea_key =  configfile.readline().rstrip()
        linea_hash = configfile.readline().rstrip()
key = linea_key.replace("key=","")
hash = linea_hash.replace("hash_elegido=","")

byte_key = bytes(key, 'UTF-8')

def comprobarEnServidor(mensaje_recibido,nonceServ):
    resultado = ""
    string_separado = mensaje_recibido.split()
    datos_mensaje = string_separado[0]+" "+ string_separado[1]+ " " +string_separado[2]+" " + str(nonceServ)
    mac_En_Servidor = hmac.new(byte_key,datos_mensaje.encode('utf-8'), hash).hexdigest()
    nonceServ +=1
    if string_separado[4] == mac_En_Servidor:
        resultado = "\nComprobación correcta"
    else:
        resultado = "\nComprobación incorrecta"
    return resultado

#Generamos un nuevo socket
socketServidor = socket(AF_INET, SOCK_STREAM)
#Establecemos la conexión
socketServidor.bind( (direccionServidor,puertoServidor) )
socketServidor.listen()


#Establecemos la conexión
socketConexion, addr = socketServidor.accept()
print("Conectando con un cliente", addr)
#recibimos el mensaje del cliente
mensajeRecibido = socketConexion.recv(4096).decode()
comprobacion=comprobarEnServidor(mensajeRecibido,nonceServ)
socketConexion.send(("Se ha recibido el mensaje, se va a realizar la comprobación \n" + comprobacion).encode())
#socketConexion.send(comprobacion.encode())

print("Desconectado el cliente", addr)
#aqui hacer el log

#cerramos conexion
socketConexion.close()

# while True:
#     #Establecemos la conexión
#     socketConexion, addr = socketServidor.accept()
#     print("Conectando con un cliente", addr)
#     while True:
#         #recibimos el mensaje del cliente
#         mensajeRecibido = socketConexion.recv(4096).decode()
#         print(mensajeRecibido)

#         #esta condicion no se cumplira hasta que la cadena sea adios
#         if mensajeRecibido == 'adios':
#             break
#         #mandamos mensaje al cliente
#         socketConexion.send(input().encode())

#     print("Desconectado el cliente", addr)
#     #cerramos conexion
#     socketConexion.close()