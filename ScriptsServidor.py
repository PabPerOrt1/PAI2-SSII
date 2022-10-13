from socket import *
import hmac,os

direccionServidor = "localhost"
puertoServidor = 9899

with open("Config.config") as configfile:
        linea_key =  configfile.readline().rstrip()
        linea_hash = configfile.readline().rstrip()
key = linea_key.replace("key=","")
hash = linea_hash.replace("hash_elegido=","")

byte_key = bytes(key, 'UTF-8')

def comprobarEnServidor(mensaje_recibido):
    with open('nonce_utilizados.txt','r') as noncefile:
            var = noncefile.readlines()
    resultado = ""
    string_separado = mensaje_recibido.split()
    datos_mensaje = string_separado[0]+" "+ string_separado[1]+ " " +string_separado[2]+" " + string_separado[3]
    mac_En_Servidor = hmac.new(byte_key,datos_mensaje.encode('utf-8'), hash).hexdigest()
    if string_separado[4] == mac_En_Servidor and (string_separado[3]+'\n') not in var:
        resultado = "Comprobación correcta\n"
    else:
        resultado = "Comprobación incorrecta\n"
    return [resultado,string_separado[3]]

#Generamos un nuevo socket
socketServidor = socket(AF_INET, SOCK_STREAM)
#Establecemos la conexión
socketServidor.bind((direccionServidor,puertoServidor))
socketServidor.listen()

directorio_listado = os.listdir("./Ficheros_de_Prueba")

#Establecemos la conexión

for archivo in directorio_listado:
    socketConexion, addr = socketServidor.accept()
    print("Nueva Prueba", addr)

#recibimos el mensaje del cliente
    mensajeRecibido = socketConexion.recv(4096).decode()
    comprobacion=comprobarEnServidor(mensajeRecibido)
    socketConexion.send(("Se ha recibido el mensaje, se va a realizar la comprobacion \n" + comprobacion[0]+'\n').encode())
    #Guardar Nonce y Log
    if comprobacion[0] == "Comprobación incorrecta\n":
        with open('nonce_utilizados.txt','r') as noncefile:
            var = noncefile.readlines()
            if (comprobacion[1]+'\n') in var:
                with open('log.txt','a') as logfile:
                    logfile.write("Hubo un error por reply attack, el nonce " + comprobacion[1] + " esta repetido\n")
            else:
                with open('log.txt','a') as logfile:
                    logfile.write("Hubo un error por man-in-the-middle\n")
    else:
        with open('nonce_utilizados.txt','a') as f:
            f.write(comprobacion[1]+'\n')

#cerramos conexion
print("Desconectado el cliente", addr)
socketConexion.close()