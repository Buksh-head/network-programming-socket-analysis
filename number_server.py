from echo_server import EchoServer
import socket
import sys


class NumberServer(EchoServer):
    """
    Inherit from echo_server.py
    """
    def __init__(self):
        super().__init__()

    def convert_message(self, recv_data):
        """
        Convert numerical digits into their verbal equivalents
        :param recv_data: data received from the client
        :return: the converted verbal equivalents if numerical
        digits is provided, otherwise return "Invalid message"
        """
        number_word_mapping = {
        '0': "zero",
        '1': "one",
        '2': "two",
        '3': "three",
        '4': "four",
        '5': "five",
        '6': "six",
        '7': "seven",
        '8': "eight",
        '9': "nine"
        }

        msg = "[Server] " + number_word_mapping.get (recv_data, "Invalid message")

        return msg

    def receive_and_send_messages(self):
        """
        Use a while loop to continuously receive, convert and
        send messages to the client.
        :return: None
        """
        self.conn, addr = self.socket.accept()
        while True:
            self.send_message(self.convert_message(self.receive_message()))

    def run_number_server(self):
        """
        Start the number server to receive, convert and
        send back messages to the client
        :return: None
        """
        self.read_port_number()
        self.listen_on_port()
        self.receive_and_send_messages()


if __name__ == '__main__':
    number_server = NumberServer()
    number_server.run_number_server()