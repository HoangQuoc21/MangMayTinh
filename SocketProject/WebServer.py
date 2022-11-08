#Thêm Thư Viện Để Sử Dụng Các Hàm Liên Quan
import socket 
import threading
from os import error

#Khai báo thông tin của Host address và Port Sử Dụng
HOST = '127.0.0.1'
PORT = 8080

#Tạo Socket Server với dạng địa chỉ IPv4 và giao thức TCP/IP (Có Kết Nối)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind Server Socket đã tạo ở trên lên 
SERVER.bind((HOST, PORT))

#Hàm để xử lý Request từ Client. Parse Request Và Gửi Trả Data về
def handle(client, addr):
    while True:
        data = client.recv(1024).decode()
        if not data: break
        print(data)
        
        #Đóng Kết Nối Client
        client.close()
        break


#Cho Server Mở Kết Nối Để Lắng Nghe 
def start():
    SERVER.listen()
    while True:
        #Chấp nhận Kết Nối từ Client 
        conn, addr = SERVER.accept()
        thread = threading.Thread(target= handle, args=(conn, addr))
        thread.start()
    
    
if __name__ == '__main__':
    start()