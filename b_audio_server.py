from vidstream import AudioSender
from vidstream import AudioReceiver
import threading
import socket

ip = socket.gethostbyname(socket.gethostname())
receiver= AudioReceiver(ip,9988)
receive_thread=threading.Thread(target=receiver.start_server)

sender = AudioSender(ip,9988)
sender_thread=threading.Thread(target=sender.start_stream)

receive_thread.start()
sender_thread.start()
