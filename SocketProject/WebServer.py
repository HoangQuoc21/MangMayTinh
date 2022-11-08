#Thêm Thư Viện Để Sử Dụng Các Hàm Liên Quan
import socket 
import threading
# import error là thư viện chứa các lỗi có thể xảy ra khi lập trình 
from os import error

#Khai báo thông tin của Host address và Port Sử Dụng
HOST = '127.0.0.1'
PORT = 8080

#Tạo Socket Server với dạng địa chỉ IPv4 và giao thức TCP/IP (Có Kết Nối)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#Bind Server Socket đã tạo ở trên lên, Nếu lỗi thì in thông báo ra ternimal 
try:
    SERVER.bind((HOST,PORT))
    #In lên Terminal xem WebServer đang chạy tại địa chỉ nào
    print(f'\n* Server running on http://{HOST}:{PORT} *\n')
    #Nếu socket gặp lỗi thì sẽ báo lên terminal: 
except socket.error as e:
    print(f'Socket error: {e}\n')
    print('Socket error: %s\n' %(e))

#Hàm trả về response_header tương ứng với từng loại content_type
def response_header(Content_type):
    message_header = 'HTTP/1.1 200 \n'
    message_header += f'Content-type: {Content_type}'
    message_header += '\r\n\r\n'
    message_header = message_header.encode()
    return message_header

#Hàm đọc nội dung file và chuyển data đã đọc về dưới dạng nhị phân (byte)
def read_file(file_url, Content_type):
    f = open(file_url, 'rb')
    f_data = response_header(Content_type)
    f_data += f.read()
    return f_data


#Hàm handle để xử lý Request từ Client. Parse Request Và Gửi Trả Data về
def handle(client, addr):
    while True:
        #Nhận data là Request từ Client
        data = client.recv(1024).decode()
        #Nếu không có data thì thoát khỏi vòng lặp
        if not data: break
        
        #Phân tích Request Từ Data nhận về
        request_line = data.split('\r\n')[0]
        request_method = request_line.split(' ')[0]
        request_url = request_line.split(' ')[1]

        #print(data)
        print(request_line)
        print(request_method)
        print(request_url)
        
        #Xử lý các kiểu dữ liệu trả về nếu method là GET:
        if request_method == 'GET':
            if request_url == '/' or request_url == '/index.html':
                url = 'D:/Github/MangMayTinh/SocketProject/index.html'
                Content_type = 'text/html'
                #SendBackData (nhị phân) là dữ liệu đọc từ hàm read_file (bao gồm response_header và nội dung file đọc tương ứng)   
                sendBackData = read_file(url, Content_type)
            elif request_url == '/css/style.css':
                url = 'D:/Github/MangMayTinh/SocketProject/css/style.css'
                Content_type = 'text/css'
                #SendBackData (nhị phân) là dữ liệu đọc từ hàm read_file (bao gồm response_header và nội dung file đọc tương ứng)   
                sendBackData = read_file(url, Content_type)
            elif request_url == '/favicon.ico':
                url = 'D:/Github/MangMayTinh/SocketProject/favicon.ico'
                Content_type = 'image/x-icon'
                sendBackData = read_file(url, Content_type)
            elif(request_url.split('/')[1] == 'avatars'): 
                if request_url == '/avatars/1.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/1.png'
                elif request_url == '/avatars/2.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/2.png'
                elif request_url == '/avatars/3.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/3.png'
                elif request_url == '/avatars/4.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/4.png'
                elif request_url == '/avatars/5.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/5.png'
                elif request_url == '/avatars/6.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/6.png'
                elif request_url == '/avatars/7.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/7.png'
                elif request_url == '/avatars/8.png':
                    url = 'D:/Github/MangMayTinh/SocketProject/avatars/8.png'
                Content_type = 'image/png'
                #SendBackData (nhị phân) là dữ liệu đọc từ hàm read_file (bao gồm response_header và nội dung file đọc tương ứng)   
                sendBackData = read_file(url, Content_type)
            else:
                #Nếu Load Page Không Đúng Thì Trả Về 404.html
                url = 'D:/Github/MangMayTinh/SocketProject/404.html'
                Content_type = 'text/html'
                sendBackData = read_file(url, Content_type)
                
            #Gửi nội dung data đã đọc lại cho client
            client.send(sendBackData)
        
        #Đóng Kết Nối Client
        client.close()
        break

#Cho Mở Kết Nối Server Để Lắng Nghe Kết Nối Từ Client
def start():
    SERVER.listen()
    while True:
        #Chấp nhận Kết Nối từ Client 
        conn, addr = SERVER.accept()
        #Thread dùng để xử lý nhiều request trong 1 kết nối
        thread = threading.Thread(target= handle, args=(conn, addr))
        thread.start()
    
    
if __name__ == '__main__':
    start()