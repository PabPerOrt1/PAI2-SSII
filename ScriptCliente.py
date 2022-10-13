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
# def crear_mensaje():
#     nonceClient = secrets.randbelow(9999)
#     cuenta_origen = input("Indique la cuenta origen: ")
#     cuenta_dest = input("Indique la cuenta destino: ")
#     cantidad = input("Teclee la cantidad: ")

#     datos_mensaje= cuenta_origen+" "+ cuenta_dest+" "+str(cantidad)+" "+ str(nonceClient)
#     print(datos_mensaje)
    
#     mensaje_hasheado =""
#     if hash == 'sha224' or hash == 'sha256' or hash == 'sha384' or hash == 'sha512' :
#         mensaje_hasheado+=hmac.new(byte_key,datos_mensaje.encode('utf-8'), hash ).hexdigest()
#     else:
#         mensaje_hasheado+= "Hash mal escrito"
    
#     return datos_mensaje +" " +mensaje_hasheado 

def lee_mensaje():
    with open('./Ficheros_de_Prueba/'+"Prueba"+str(i)+".txt",'r') as f:
        origen = f.readline().rstrip()
        dest = f.readline().rstrip()
        cant = f.readline().rstrip()
        nonceClient = f.readline().rstrip()
    return origen, dest, cant, nonceClient

def Hash_Mensaje(mensaje):
    mensaje_hasheado =""
    if hash == 'sha224' or hash == 'sha256' or hash == 'sha384' or hash == 'sha512' :
        mensaje_hasheado+=hmac.new(byte_key,mensaje.encode('utf-8'), hash ).hexdigest()
    
    return mensaje_hasheado 

def mensajes_automaticos(cuenta_origen,cuenta_dest,cantidad,nonceClient):
    
    datos_mensaje= str(cuenta_origen)+" "+ str(cuenta_dest)+" "+str(cantidad)+" "+ str(nonceClient)

    return datos_mensaje

def fusion_mensajes(mensaje, cifrado):
    return mensaje + " " + cifrado 

directorio_listado = os.listdir("./Ficheros_de_Prueba")


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





#escribimos el mensaje
i=0
for archivo in directorio_listado:
    #se decaran e inicializaran los valores del socket del cliente
    socketCliente = socket(AF_INET, SOCK_STREAM)
    socketCliente.connect((IPServidor,puertoServidor))

    #Leer el mensaje
    origen,dest,cant,nonceClient = lee_mensaje()
    mensaje = mensajes_automaticos(origen,dest,cant,nonceClient)
    cifrado = Hash_Mensaje(mensaje)
    print("Prueba"+str(i)+ " " + fusion_mensajes(mensaje, cifrado))

    time.sleep(10)

    #Parte para MAN-IN-THE-MIDDLE
    origen2,dest2,cant2,nonceClient2 = lee_mensaje()
    mensaje2 = mensajes_automaticos(origen2,dest2,cant2,nonceClient2)
    print("Prueba"+str(i)+ " " +fusion_mensajes(mensaje2, cifrado))

    #enviamos mensaje
    socketCliente.send(fusion_mensajes(mensaje2, cifrado).encode())
    #recibimos el mensaje
    respuesta = socketCliente.recv(4096).decode()
    print(respuesta)
    i+=1

socketCliente.close()
sys.exit()