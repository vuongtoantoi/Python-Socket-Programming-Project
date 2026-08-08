from vidstream import AudioSender
from vidstream import AudioReceiver
import speech_recognition as sr
import time
import threading
import socket
def AUDIO():
    ip = socket.gethostbyname(socket.gethostname())
    receiver= AudioReceiver(ip,9988)
    receive_thread=threading.Thread(target=receiver.start_server)

    sender = AudioSender(ip,9988)
    sender_thread=threading.Thread(target=sender.start_stream)

    receive_thread.start()
    sender_thread.start()
def SPEECH_TO_TEXT():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        with microphone as source:
            print("Đang nghe...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio,language="vi-VN")
            msg= text
            print(f"Bạn nói: {msg}")
            return msg
        except sr.UnknownValueError:
            print("Xin lỗi, tôi không hiểu.")
        except sr.RequestError as e:
            print(f"Không giải quyết được; {e}")
if __name__ == "__main__":
    audio_thread = threading.Thread(target=AUDIO)
    speech_thread = threading.Thread(target=SPEECH_TO_TEXT)

    audio_thread.start()
    time.sleep(1)  # Ensure audio starts before speech recognition
    speech_thread.start()

    audio_thread.join()
    speech_thread.join()
    