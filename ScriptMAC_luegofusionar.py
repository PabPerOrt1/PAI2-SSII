import hmac 
from hashlib import sha224,sha256,sha384,sha512

cantidad = input("Teclee la cantidad: " )
cuenta_origen = input("Indique la cuenta origen: ")
cuenta_dest = input("Indique la cuenta destino: ")

datos_mensaje= cuenta_origen+" "+ cuenta_dest+" "+str(cantidad)
print(datos_mensaje)
with open("Config.config") as configfile:
    linea_key =  configfile.readline().rstrip()
    linea_hash = configfile.readline().rstrip()

key = linea_key.replace("key=","")
hash = linea_hash.replace("hash_elegido=","")

byte_key = bytes(key, 'UTF-8')
mensaje = datos_mensaje.encode()

def funcionMac():
    mac_devuelto =""
    if hash == 'sha224' or hash == 'sha256' or hash == 'sha384' or hash == 'sha512' :
        mac_devuelto+=hmac.new(byte_key,mensaje, hash ).hexdigest()
    else:
        mac_devuelto+= "Hash mal escrito"
    return mac_devuelto

mensaje_De_Cliente_A_Servidor = [datos_mensaje,funcionMac()]

def comprobarEnServidor(mensaje_recibido):
    resultado = ""
    mac_En_Servidor = hmac.new(byte_key,mensaje_recibido[0].encode('utf-8'), hash).hexdigest()
    print(mac_En_Servidor)
    if mensaje_recibido[1] == mac_En_Servidor:
        resultado = "Bien hecho"
    else:
        resultado = "Mal"
    return resultado

print(funcionMac())
print(comprobarEnServidor(mensaje_De_Cliente_A_Servidor))