import socket

ip = '10.100.217.16'
port = 6666
BUF_SIZE = 1024
mensajePrueba = "Prueba"

k = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)

k.connect((ip,port))

k.send(mensajePrueba.encode('utf-8'))
data = k.recv(BUF_SIZE)
k.close