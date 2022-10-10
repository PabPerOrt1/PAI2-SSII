from socket import *
import hmac

direccionServidor = "localhost"
puertoServidor = 9899
nonceServ=1

with open("Config.config") as configfile:
        linea_key =  configfile.readline().rstrip()
        linea_hash = configfile.readline().rstrip()
key = linea_key.replace("key=","")
hash = linea_hash.replace("hash_elegido=","")

byte_key = bytes(key, 'UTF-8')

def comprobarEnServidor(mensaje_recibido):
    resultado = ""
    string_separado = mensaje_recibido.split()
    datos_mensaje = string_separado[0]+" "+ string_separado[1]+ " " +string_separado[2]+" " + string_separado[3]
    mac_En_Servidor = hmac.new(byte_key,datos_mensaje.encode('utf-8'), hash).hexdigest()
    if string_separado[4] == mac_En_Servidor:
        resultado = "\nComprobación correcta"
    else:
        resultado = "\nComprobación incorrecta"
    return [resultado,string_separado[3]]

#Generamos un nuevo socket
socketServidor = socket(AF_INET, SOCK_STREAM)
#Establecemos la conexión
socketServidor.bind((direccionServidor,puertoServidor))
socketServidor.listen()


#Establecemos la conexión
socketConexion, addr = socketServidor.accept()
print("Conectando con un cliente", addr)
#recibimos el mensaje del cliente
mensajeRecibido = socketConexion.recv(4096).decode()
comprobacion=comprobarEnServidor(mensajeRecibido)
socketConexion.send(("Se ha recibido el mensaje, se va a realizar la comprobación \n" + comprobacion[0]).encode())
#Guardar Nonce y Log
if comprobacion[0] == "\nComprobación incorrecta":
    with open('nonce_utilizados.txt','r') as noncefile:
        var = noncefile.readlines()
        if comprobacion[1] in var:
            with open('log.txt','a+') as logfile:
                logfile.write("Hubo un error por reply attack, el nonce " + comprobacion[1] + " está repetido")
        else:
            with open('log.txt','a+') as logfile:
                logfile.write("Hubo un error por man-in-the-middle")
else:
    with open('nonce_utilizados.txt','a+') as f:
        f.write(comprobacion[1])

print("Desconectado el cliente", addr)

#cerramos conexion
socketConexion.close()