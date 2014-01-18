import sys
import socket
import select
#===============================================================================
# from multiprocessing import Queue
# import hashlib
# import urllib.request as urllib
#===============================================================================

port=56213
#===============================================================================
# bootstrap={urllib.urlopen("http://myip.dnsdynamic.org/").read():[
#         (urllib.urlopen("http://myip.dnsdynamic.org/").read(),port)]}
#===============================================================================
class Mesh(object):
	def __init__(self,bucket=None,ip='',port=0):
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.port=port
		self.ip=ip
		try:
			self.sock.bind((self.ip,self.port))
		except:
			print('The port was taken')
			self.sock.bind(('',0))
		self.sock.setblocking(0)
		self.port2=self.sock.getsockname()[1]
		if self.sock.getsockname()[0]=='0.0.0.0':
			self.ip='127.0.0.1'
		self.myaddr=(self.ip,self.port2)
		self.waiting=set()
		if bucket is not None:
			print(bucket)
			self.bucket=bucket
		else:
			self.bucket={}
		
	def main(self):
		running=True
		while running:
			ins,outs,ers=[self.sock],[self.sock],[]
			inc,outg,errs=select.select(ins,outs,ers)
			if inc:
				self.get(inc[0])
			#===================================================================
			# for o in outg:
			# 	self.send(test,o,self.myaddr)
			#===================================================================
			
			#if IDpacket[0] number not in some list : do_something
			#if IDpacket[1] not in some list: add_to_list and do_something_else
			#if flagData[0] == something: queue append
			#if flagData[0] == soemthing_else: append other queue
			#etc
		#if something in queue: for writesocket in out: sendto()			
	def get(self,sock,buff=8192):
		data,host=sock.recvfrom(buff)
		flag,number,uid,data=self.u_pack(data)
		inwaiting=self._inwaiting(number,host)
		self._ifflag(flag,inwaiting,uid,data,host)
		self.to_bucket(uid,host)

	def send(self,data,sock,addr):
		flag,number,uid,data=self.u_pack(data)
		sock.sendto((flag+number+uid+data),addr)
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
	def _inwaiting(self,number,host):
		if (number,host) in self.waiting:
			return True
		else:
			self.waiting.add((number,host))
			return False
	def _ifflag(self,flag,inwaiting,uid,data,host):
		if flag == 1:
			if inwaiting:
				pass
		if flag == 2:
			pass
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
	def to_bucket(self,uid,host,full=None):
		if full is None:
			full=8
		if len(self.bucket)>=full:	#max dict keys  (max size =full*(256**2))
			return
		ip,port = host
		if uid not in self.bucket.keys():
			self.bucket[uid]=(ip,port)
		else: #There's more work to be done on this.
			if host not in self.bucket[uid]:
				self.bucket[uid]=(ip,port)
				
if __name__ == '__main__':
	b=Mesh(port=port)
	b.main()
