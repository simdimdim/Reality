import net
import threading

#===============================================================================
# class Main(threading.Thread):
# 	def __init__(self):
# 		threading.Thread.__init__(self)
# 		self.Channels=connections.Channels()
# 	def run(self):
# 		self.Channels.listen()
#===============================================================================

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
