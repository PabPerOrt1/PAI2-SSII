from asyncio.windows_utils import BUFSIZE
import socket

ip='10.100.217.16'
port= 60
BUF_SIZE=30
k = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
k.bind((ip,port))
k.listen(1)

con,addr = k.accept()
print("Conecction addres is: " + addr)
while True:
    data = con.recv(BUF_SIZE)
    if not data:
        break
print("Received data",data)
con.send(data)
con.close()