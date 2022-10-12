from socket import *
import secrets
from hashlib import sha224,sha256,sha384,sha512
import sys , hmac, time, os

IPServidor = "localhost"
puertoServidor = 9899

with open("Config.config") as configfile:
        linea_key =  configfile.readline().rstrip()
        linea_hash = configfile.readline().rstrip()
key = linea_key.replace("key=","")
hash = linea_hash.replace("hash_elegido=","")

byte_key = bytes(key, 'UTF-8')



#Se recojen los datos del mensaje y se le aplica algoritmo HMAC
def crear_mensaje():
    nonceClient = secrets.randbelow(9999)
    cuenta_origen = input("Indique la cuenta origen: ")
    cuenta_dest = input("Indique la cuenta destino: ")
    cantidad = input("Teclee la cantidad: ")

    datos_mensaje= cuenta_origen+" "+ cuenta_dest+" "+str(cantidad)+" "+ str(nonceClient)
    print(datos_mensaje)
    
    mensaje_hasheado =""
    if hash == 'sha224' or hash == 'sha256' or hash == 'sha384' or hash == 'sha512' :
        mensaje_hasheado+=hmac.new(byte_key,datos_mensaje.encode('utf-8'), hash ).hexdigest()
    else:
        mensaje_hasheado+= "Hash mal escrito"
    
    return datos_mensaje +" " +mensaje_hasheado 

def mensajes_automaticos():
    nonceClient = secrets.randbelow(9999)
    directorio_listado = os.listdir("./Ficheros_de_Prueba")
    for archivo in directorio_listado:
        with open('./Ficheros_de_Prueba/' + archivo,'r') as f:
            cuenta_origen = f.readline().rstrip()
            cuenta_dest = f.readline().rstrip()
            cantidad = f.readline().rstrip()

    datos_mensaje= cuenta_origen+" "+ cuenta_dest+" "+str(cantidad)+" "+ str(nonceClient)
    print(datos_mensaje)
    
    mensaje_hasheado =""
    if hash == 'sha224' or hash == 'sha256' or hash == 'sha384' or hash == 'sha512' :
        mensaje_hasheado+=hmac.new(byte_key,datos_mensaje.encode('utf-8'), hash ).hexdigest()
    else:
        mensaje_hasheado+= "Hash mal escrito"
    
    return datos_mensaje +" " +mensaje_hasheado 


# #se decaran e inicializaran los valores del socket del cliente
# socketCliente = socket(AF_INET, SOCK_STREAM)
# socketCliente.connect((IPServidor,puertoServidor))
# #escribimos el mensaje
# mensaje = crear_mensaje()
# #aqui meter la inyeccion, hacer otra funcion de mensaje

# #enviamos mensaje
# socketCliente.send(mensaje.encode())
# #recibimos el mensaje
# respuesta = socketCliente.recv(4096).decode()
# print(respuesta)
# socketCliente.close()
# sys.exit()

#se decaran e inicializaran los valores del socket del cliente
socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((IPServidor,puertoServidor))

i=0
while i <= 1001:    
    i+=1
    #escribimos el mensaje
    mensaje = mensajes_automaticos()
    print(mensaje)
    #aqui meter la inyeccion, hacer otra funcion de mensaje

    #enviamos mensaje
    socketCliente.send(mensaje.encode())
    #recibimos el mensaje
    #respuesta = socketCliente.recv(4096).decode()
    #print(respuesta)
    time.sleep(10)

socketCliente.close()
sys.exit()