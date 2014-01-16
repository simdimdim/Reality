import threading
import time
import socket
import random

class DHT:
	def __init__(self):
		pass
	def listen(self):
		pass




a=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	port=63412
	a.bind(('',port))
except:
	a.bind(('',0))
	port=a.getsockname()[1]
print(a.getsockname())
addr=('192.168.1.9',port)
addr=addr
c=1
while c<10:
	if random.randint(0,8)<=7:
		data=bytes(str(c),'ascii')
		a.sendto(data,addr)
	data,host=a.recvfrom(2048)
	if data:
		print(data.decode(),host)
	if not data:
		break
	c+=1