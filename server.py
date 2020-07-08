import socket

class Servidor:
	def __init__(self, host, port, ruta_video):
		self.host = host
		self.port = port 
		self.servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.ruta_video = ruta_video

		#Servidor escucha.
		#self.bind_listen() TCP
		self.servidor.bind(('', self.port))
		#Aceptamos la conexión.
		self.aceptar_conexiones()

	#def bind_listen(self):
	#	self.servidor.bind((self.host, self.port))
	#	self.servidor.listen()
	#	print('Servidor escuchando...')

	def conseguir_video(self):
		with open(self.ruta_video, 'rb') as video:
			bytes_video = video.read()
		return bytes_video


	def aceptar_conexiones(self):
		#Si quisiesemos recibir mas de una conexión hariamos uso de Threads
		#Ahora como sabemos que solo se conectará una persona solamente
		#No hacemos uso de Thread
		#cliente, address = self.servidor.accept()
		#print('Conexión establecida')

		#Recibimos el mensaje del cliente.
		data, address_cliente = self.servidor.recvfrom(4096) #Acá tenemos el address
		print(data, address_cliente)


		#Por como conformamos el cliente, sabemos que primero mandamos el tamaño
		#del archivo
		bytes_video = self.conseguir_video() #Conseguimos los bytes
		tamaño_archivo = len(bytes_video).to_bytes(4, byteorder = 'big') #Conseguimos el tamaño
		#Mandamos entonces el tamaño en bytes primero y el video despues
		self.servidor.sendto(tamaño_archivo, address_cliente)
		while len(bytes_video) > 0:
			bytes_a_enviar = bytes_video[:4096]
			if len(bytes_video) < 4097:
				bytes_video = bytes_video
			else:
				bytes_video = bytes_video[4097:]
			self.servidor.sendto(bytes_a_enviar, address_cliente) 
		print('Video enviado!')


if __name__ == '__main__':
	host = '25.14.40.70'
	port = 8000
	ruta_video = 'brightside.mp4'

	servidor = Servidor(host, port, ruta_video)