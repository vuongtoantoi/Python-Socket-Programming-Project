from vidstream import CameraClient
from vidstream import StreamingServer
import socket
import threading
import time
receiving = None
sending = None
def start_call():
    global receiving, sending
    ip = socket.gethostbyname(socket.gethostname())
    receiving= StreamingServer(ip,9999)
    sending = CameraClient(ip,9999)

    t1= threading.Thread(target=receiving.start_server)
    t1.start()

    time.sleep(2)

    t2=threading.Thread(target=sending.start_stream)
    t2.start()
def stop_call():
    print("Enter 'Enter' on the keyboards to stop the call.")
    if input() == '':
        receiving.stop_server()
        sending.stop_stream()

if __name__ == "__main__":
    start_call()
    stop_call()
