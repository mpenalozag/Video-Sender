import socket


class Cliente:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		try:
			self.reconocimiento()
			bytes_video = self.recibir_video()
			self.conseguir_video(bytes_video)
		except ConnectionError:
			print('Error al conectarse, el tontito de Martin se equivoco programando...F')
		finally:
			self.cliente.close()

	def reconocimiento(self):
		self.cliente.sendto('Este soy yo'.encode('utf-8'), (self.host, self.port))

	def recibir_video(self):
		# Primero recibimos el tamaño en bytes de el archivo
		# Esos primeros 4 bytes contienen el tamaño.
		tamaño_bytes, address = self.cliente.recvfrom(4)
		largo_archivo = int.from_bytes(tamaño_bytes, byteorder='big')
		video = bytearray()
		print('Cargando el video...')

		while len(video) < largo_archivo:
			cantidad_bytes_a_procesar = min(4096, largo_archivo - len(video))
			parte_del_video, address = self.cliente.recvfrom(cantidad_bytes_a_procesar)
			video.extend(parte_del_video)
			print(f'{len(video)}/{largo_archivo} bytes completados')
		print('Video Cargado!')
		return video #Va a retornar los bytes que conforman el video

	def conseguir_video(self, bytes_video):
		with open('video_prueba_2.mp4', 'wb') as video:
			video.write(bytes_video)

		print('Listo! Ahora tienes el video!')

if __name__ == '__main__':
	host = '25.14.40.70'   
	port = 8000

	cliente = Cliente(host, port)