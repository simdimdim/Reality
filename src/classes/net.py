import sys
import socket
import select
#===============================================================================
# from multiprocessing import Queue
# import hashlib
# import urllib.request as urllib
#===============================================================================

port=56213
#bootstrap={urllib.urlopen("http://myip.dnsdynamic.org/").read():[
#        (urllib.urlopen("http://myip.dnsdynamic.org/").read(),port)]}
class Mesh(object):
	def __init__(self,bootstrap=dict(),ip='',port=0,timeout=20):
		self.ip=ip
		self.port=port
		self.timeout=timeout
		self.bootstrap=bootstrap
		self.waiting=set()
		self.setup()
	def main(self):
		self.incoming=[self.sock]
		self.outgoing=[self.sock]
		self.err=[]
		running=True
		test=(1,1,1,'string')
		self.send(test,('localhost',port))
		while running:
			try:
				inp,out,err=select.select(self.incoming,self.outgoing,
										self.err,self.timeout)
				for sock in inp:
					self.get(sock)
					#if IDpacket[0] number not in some list : do_something
					#if IDpacket[1] not in some list: add_to_list and do_something_else
					#if flagData[0] == something: queue append
					#if flagData[0] == soemthing_else: append other queue
					#etc
				#if something in queue: for writesocket in out: sendto()
			except:
				print('select?! Y U NO WORK')
	def get(self,sock,buff=8192):
		try:
			data,host=sock.recvfrom(buff)
			flag,number,uid,data=self.u_pack(data)
			inwaiting=self._inwaiting(number,host)
			self._ifflag(flag,inwaiting,uid,data,host)
			self.to_bucket(uid,host)
		except:
			print("Can't get")
	def send(self,data,addr):
		flag,number,uid,data=self.u_pack(data)
		self.sock.sendto((flag+number+uid+data),addr)
	def _ifflag(self,flag,inwaiting,uid,data,host):
		if flag == 1:
			if inwaiting:
				pass
		if flag == 2:
			pass
	def _inwaiting(self,number,host):
		if (number,host) in self.waiting:
			return True
		else:
			self.waiting.add((number,host))
			return False
	def u_pack(self,data,flagbytes=(0,1),nbytes=(1,3),
			idbytes=(3,9),databytes=9):
		if isinstance(data,tuple):
			flag,number,uid,data=data
		else:
			try:
				flag=data[flagbytes[0]:flagbytes[1]]
				number=data[nbytes[0]:nbytes[1]]
				uid=data[idbytes[0]:idbytes[1]]
				data=data[databytes:]
			except:
				print('error, packet too something')
		flag = self._intconv( flag, byte=(flagbytes[1]-flagbytes[0]) )
		number = self._intconv( number, byte = (nbytes[1]-nbytes[0]) )
		uid = self._intconv( uid, byte = (idbytes[1]-idbytes[0]) )
		data = self._strconv(data)
		return (flag,number,uid,data)
	def _strconv(self,data):
		if isinstance(data,bytes):
			try:
				return data.decode()				
			except:
				print("Can't decode data")
		else:
			try:
				return bytes(str(data),'ascii')
			except:
				print("Can't encode data")	
	def _intconv(self,element,byte=1):
		if isinstance(element,bytes):
			try:
				return int.from_bytes(element,byteorder='little')
			except:
				print("Can't decode int")
		else:
			try:
				return element.to_bytes(byte,byteorder='little')
			except:
				print('Probably int too big to fit in bytes')
	#Setup, bucket
	def to_bucket(self,uid,host,bucket=None,full=None):
		if bucket is None:
			bucket=self.bootstrap
		if full is None:
			full=8
		if len(bucket)>=full:	#max dict keys  (max size =full*(256**2))
			return
		ip,port = host
		if uid not in bucket.keys():
			bucket[uid]=(ip,port)
		else:
			if host not in bucket[uid]:
				bucket[uid]=(ip,port)
		self.bootstrap=bucket

	#Auto Config & Checks
	def setup(self):
		try:
			self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except:
			print('socks problems1')
		try:
			self.sock.bind((self.ip,self.port))
		except:
			try:
				self.sock.bind(('',self.port))
			except:
				print('The port is taken')
				try:
					self.sock.bind(('',0))
				except:
					self.sock.close()
					print("Can't bind. Something is wrong with the socket")
		try:
			self.port=self.sock.getsockname()[1]
		except:
			print("Can't even get it's fucking name?!")
		if self.sock.getsockname()[0]=='0.0.0.0':
			self.myaddr=('127.0.0.1',self.port)
		else:
			self.myaddr=self.sock.getsockname()
		self.ip=self.myaddr[0]
		self.sock.setblocking(0)
		
if __name__ == '__main__':
	a=Mesh(port=port)
	a.main()

#===============================================================================
# Problem running this as an import
#===============================================================================