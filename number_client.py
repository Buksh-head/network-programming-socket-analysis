from echo_client import EchoClient
import socket
import sys


class NumberClient(EchoClient):
    
    def __init__(self):
        super().__init__()

    def send_message(self):
        """ 
        Read messages from stdin, then convert to bytes and
        send out as a TCP packets
        :return: None
        """
        msg = input().strip()
        while not msg:
            print("[Server] Invalid message")
            msg = input().strip()
        self.socket.send(msg.encode())

if __name__ == "__main__":
    number_client = NumberClient()
    number_client.run_client()
