import socket
import threading
import time
from vidstream import AudioReceiver
from vidstream import AudioSender
from vidstream import CameraClient
from vidstream import StreamingServer

receiver=AudioReceiver('192.168.56.1', 5555)
receive_thread=threading.Thread(target=receiver.start_server)

sender=AudioSender('192.168.56.1',4444)
sender_thread=threading.Thread(target=sender.start_stream)

camera_sender=StreamingServer('192.168.56.1',3333)
camera_sender_thread=threading.Thread(target=camera_sender.start_server)

camera_receiver=CameraClient('192.168.56.1',2222)
camera_receive_thread=threading.Thread(target=camera_receiver.start_stream)


receive_thread.start()
time.sleep(2)
sender_thread.start()

camera_sender_thread.start()
time.sleep(2)
camera_receive_thread.start()