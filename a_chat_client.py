import socket
import threading
import tkinter
from tkinter import simpledialog

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
client.connect((ip,3333))

print('Connected to the server!')

class GUI:
    def __init__(self):
        self.window=tkinter.Tk()
        self.window.withdraw()
        
        self.nickname=simpledialog.askstring('Name','Please choose a nickname',parent=self.window)
        self.nickname=self.nickname if self.nickname else 'Anonymous'

        self.chat_window=tkinter.Toplevel(self.window)
        self.chat_window.title('Chat Room')

        self.text_area=tkinter.Text(self.chat_window)
        self.text_area.pack()

        # Nut gui tin nhan
        self.msg_entry=tkinter.Entry(self.chat_window)
        self.msg_entry.pack()
        self.msg_entry.bind('<Return>',self.send_message)
        send_button = tkinter.Button(self.chat_window, text="Send", command=self.send_message)
        send_button.pack(side=tkinter.BOTTOM)

        #Nut gui tin nhan bang audio
        voice_button = tkinter.Button(self.chat_window, text="Voice Message",command=self._handle_voice_click)
        voice_button.pack(side=tkinter.LEFT)

        #Nut goi video
        camera_button = tkinter.Button(self.chat_window, text="Video Call",command=self._handle_camera_click)
        camera_button.pack(side=tkinter.LEFT)

        self.window.protocol('WM_DELETE_WINDOW',self.on_closing)

        receive_thread=threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.window.mainloop()
    def receive_messages(self):
        while True:
            try:
                message=client.recv(1024).decode('utf-8')
                if message=='NICK':
                    client.send(self.nickname.encode('utf-8'))
                else:
                    self.text_area.insert(tkinter.END,message+'\n')
            except:
                print('An error occurred!')
                client.close()
                break
    def send_message(self,event=None):
        message=f'{self.nickname}: {self.msg_entry.get()}'
        client.send(message.encode('utf-8'))
        self.msg_entry.delete(0,tkinter.END)
    def on_closing(self):
        self.window.destroy()
        client.close()
    
    def _handle_voice_click(self):
        try:
            import b_audio_client
            text = b_audio_client.SPEECH_TO_TEXT()
            if text:
                message = f'{self.nickname} (voice): {text}'
                client.send(message.encode('utf-8'))
        except Exception as e:
            print(f'Error during speech-to-text: {e}')
    def _handle_camera_click(self):
        try:
            import camerachat
            camerachat.start_call()
            camerachat.stop_call()
        except Exception as e:
            print(f'Error during video call: {e}') 
if __name__ == "__main__":
    gui=GUI()
