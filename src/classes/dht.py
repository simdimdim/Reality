import net
import threading

def mesh():
	a=net.Mesh()
	a.main()
	
class DHT:
	def __init__(self,connectionsobj=net.Mesh()):
		pass
	def listen(self):
		pass
	def initiate(self,bootstrap=None):
		#if bootstrap is None:
			#bootstrap=self.bootstrap
		pass
	def update(self,connections,bootstrap):
		pass
if __name__ == '__main__':
	Mesh=threading.Thread(target=mesh)
	Mesh.start()
