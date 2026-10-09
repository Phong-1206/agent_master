import socket 
import threading

class ClientAgent:
    def __init__(self, host="127.0.0.1", port= 65432):
        self.host = host
        self.port = port 
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = True
    
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            
        except Exception as e:
            print("[CLIENT] Không thể kết nối với máy chủ.")
            return
    def listen_to_server(self):
        while self.is_running:
            try:
                data = self.client_socket.recv(1024).decode("utf-8")
                if not data: 
                    break
                if data.startswith("CMD:"):
                    cmd_string = data.replace("CMD:", "")
                    threading.Thread(target=self.command, args=(cmd_string), daemon=True).start()
                    # print(cmd_string)

                else:
                    print(f"[SERVER-CHAT]: {data}")
            except:
                print("[CLIENT] Server mất kết nối.")
                break
    def command(self,cmd_string):
        try:
            self.client_socket.sendall(f"Client đã nhận được lệnh".encode("utf-8"))
            print(f"thực thi: {cmd_string}")
        except Exception as e:
            self.client_socket.sendall(f"Lỗi Thực Thi: {e}".encode("utf-8"))

if __name__ == "__main__":
    try:
        client = ClientAgent()
        client.connect()
        threading.Thread(target=client.listen_to_server, daemon=True).start()
        while True:
            pass
    except KeyboardInterrupt:
        print("Admin: Ctrl + C.")