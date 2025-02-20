import socket
import sys
import time
import threading
import os


class ChatServer:

    def __init__(self):
        self.host = "127.0.0.1"
        self.client_name = None
        self.port = None
        self.socket = None
        self.conn = None

    def read_port_number(self):
        """
        Read the port number from argument, store it to self.port.
        Exit with code 1 if invalid argument is provided.
        :return: None
        """
        if len(sys.argv) != 2:
            sys.exit(1)
        self.port = int(sys.argv[1])

    def listen_on_port(self):
        """
        Create a socket listens on the specified port.
        Store the socket object to self.socket.
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        sys.stdout.write(f"[({current_time})] Waiting for a connection\n")
        sys.stdout.flush()

    def recv_client_connection(self):
        """
        Accept a client connection and store the new
        accepted connection to self.conn.
        Get and store the client name in self.client_name.
        Print the get connection message to the stdout.
        Send the welcome message to the connected client.
        :return: None
        """
        self.conn, addr = self.socket.accept()
        self.client_name = self.conn.recv(1024).decode()
        current_time = time.strftime("%H:%M:%S", time.localtime())
        sys.stdout.write(f"[({current_time})] Get a connection from {self.client_name}\n")
        sys.stdout.flush()
        msg = f"[Server ({current_time})] Welcome to the channel, {self.client_name}"
        self.conn.send(msg.encode())

    def _receive_and_print_message(self):
        """
        Use a while loop to receive TCP packets from the client and print
        messages to stdout.
        If the message is "exit", print "[Connection terminated by the client]"
        to stdout. Then close the socket and exit wit code 0.
        :return: None
        """
        while True:
            msg = self.conn.recv(1024).decode()
            if msg == "exit" or not msg:
                sys.stdout.write("[Connection terminated by the client]")
                sys.stdout.flush()
                self.socket.close()
                os._exit(0)
            current_time = time.strftime("%H:%M:%S", time.localtime())
            if self.socket.fileno() != -1:
                sys.stdout.write(f"[{self.client_name} ({current_time})] {msg}\n")
                sys.stdout.flush()

    def receive_and_print_message(self):
        """
        Multithreading
        :return: None
        """
        threading.Thread(target=self._receive_and_print_message).start()

    def send_message(self):
        """
        Use a while loop to get message from stdin and send out the message
        back to the client.
        If the message is "exit", print "[Connection Terminated by the server]"
        to the stdout. Then close the socket and exit with code 0.
        :return: None
        """
        while True:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            input_msg = input()
            if input_msg == "exit":
                self.conn.send(input_msg.encode())
                sys.stdout.write("[Connection terminated by the server]")
                sys.stdout.flush()
                self.socket.close()
                os._exit(0)

            if input_msg != '':
                msg = f"[Server ({current_time})] " + input_msg
                self.conn.send(msg.encode())

    def run_chat_server(self):
        """
        Run the chat server that receives and sends messages to the client
        :return: None
        """
        self.read_port_number()
        self.listen_on_port()
        self.recv_client_connection()
        self.receive_and_print_message()
        self.send_message()


if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.run_chat_server()

