from socket import *
from hashlib import sha224,sha256,sha384,sha512
import sys , hmac

IPServidor = "localhost"
puertoServidor = 9899

with open("Config.config") as configfile:
        linea_key =  configfile.readline().rstrip()
        linea_hash = configfile.readline().rstrip()
key = linea_key.replace("key=","")
hash = linea_hash.replace("hash_elegido=","")

byte_key = bytes(key, 'UTF-8')

nonceClient = 1

#Se recojen los datos del mensaje y se le aplica algoritmo HMAC
def crear_mensaje(nonceClient):
    
    cuenta_origen = input("Indique la cuenta origen: ")
    cuenta_dest = input("Indique la cuenta destino: ")
    cantidad = input("Teclee la cantidad: " )
    

    datos_mensaje= cuenta_origen+" "+ cuenta_dest+" "+str(cantidad)+" "+ str(nonceClient)
    print(datos_mensaje)
    
    mensaje_hasheado =""
    if hash == 'sha224' or hash == 'sha256' or hash == 'sha384' or hash == 'sha512' :
        mensaje_hasheado+=hmac.new(byte_key,datos_mensaje.encode('utf-8'), hash ).hexdigest()
    else:
        mensaje_hasheado+= "Hash mal escrito"
    
    nonceClient+=1
    return datos_mensaje + mensaje_hasheado

#se decaran e inicializaran los valores del socket del cliente
socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((IPServidor,puertoServidor))

#escribimos el mensaje
mensaje = crear_mensaje(nonceClient)
#enviamos mensaje
socketCliente.send(mensaje.encode())
#recibimos el mensaje
respuesta = socketCliente.recv(4096).decode()
print(respuesta)
socketCliente.close()
sys.exit()

# while True:
#     #escribimos el mensaje
#     mensaje = crear_mensaje()
#     if mensaje != 'adios' :

#         #enviamos mensaje
#         socketCliente.send(mensaje.encode())
#         #recibimos el mensaje
#         respuesta = socketCliente.recv(4096).decode()
#         print(respuesta)
#     else:
#         socketCliente.send(mensaje.encode())
#         #cerramos socket
#         socketCliente.close()
#         sys.exit()
