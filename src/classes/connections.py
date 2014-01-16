import sys
import socket
import select
from multiprocessing import Queue
import hashlib
import urllib.request as urllib

port=56213
ip='127.0.0.1'
bootstrap={ip:[(ip,port)]}#{urllib.urlopen("http://myip.dnsdynamic.org/").read():
							#({urllib.urlopen("http://myip.dnsdynamic.org/").read(),port)}
def convert(data,enc='ascii'):
	try:
		return data.decode()
	except:
		return bytes(str(data),'ascii')
class Channels():
	def __init__(self,bootstrap=None,ip=None,port=None,timeout=20):
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.setup()
		self.timeout=timeout
		self.bootstrap=bootstrap
		self.listen()
	def listen(self):
		self.incoming=[self.sock]
		self.outgoing=[self.sock]
		self.err=[]
		running=True
		first=True
		count=0
		while running:
			self.test(first,count)
			try:
				inp,out,err=select.select(self.incoming,self.outgoing,self.err,self.timeout)
				for sock in inp:
					data,flag,host=self.get(sock)
			except:
				self.sock.close()
				sys.exit()
		###
	def initiate(self,bootstrap=None):
		if bootstrap is None:
			bootstrap=self.bootstrap
	def update(self,connections,bootstrap):
		pass

	#Sock,bucket Ops
	def get(self,sock,buff=2048):
		try:
			data,host=sock.recvfrom(buff)
			self.add(host)
			offset=-2
			data,flag=convert(data)[:offset],convert(data)[offset:]
			#print(data,flag)
			return data,flag,host
		except:
			pass
	def write(self,data,addr):
		data=bytes(data,'ascii')
		#packets=data.split(1024)   #The idea is to make it fit in the buffer in case it's too big.
		#for data in packets:
		self.sock.sendto(data,addr)
	def add(self,host,bucket=None,full=None):  ## TODO :add hash/node id
		if bucket is None:
			bucket=self.bootstrap
		if full is None:
			full=8
		if len(bucket)>=full:	#max dict keys  (max size =full*(256**2))
			return
		ip,port = host
		if ip in bucket.keys():
			print('notadd')
			print(bucket[ip])
			if host not in bucket[ip]:
				bucket[ip].append((ip,port))	##not complete
				print('add')
		#print(bootstrap)

	#Checks and other
	def setup(self):
		try:
			self.setaddr(ip,port)
			self.sock.bind(self.myaddr)
			self.myaddr=self.sock.getsockname()
			self.port=self.sock.getsockname()[1]
			print(self.myaddr,self.port)
		except:
			self.setaddr(ip,port)
			self.sock.bind(self.myaddr)
			self.myaddr=self.sock.getsockname()
			self.port=self.sock.getsockname()[1]
			print(self.myaddr,self.port)
	def setaddr(self,ip,port):
		if ip is not None:
			if port is not None:
				self.myaddr=(ip,port)
			else:
				self.myaddr=(ip,0)
		else:
			if port is not None:
				self.myaddr=('',port)
			else:
				self.myaddr=('',0)
	def test(self,first,count):
		if first:
			print(convert('test'),self.myaddr)
			self.sock.sendto(convert('test'),self.myaddr)
			count+=1
			first=False

if __name__ == '__main__':
	dht=Channels(bootstrap=bootstrap,port=port)
