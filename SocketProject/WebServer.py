#Thêm Thư Viện Để Sử Dụng Các Hàm Liên Quan
import socket 
#Thêm Thư Viện Threading (Đa luồng) để xử lý nhiều Client Connection đến Server cùng 1 lúc
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
    
#Hàm trả về http_header (Thông tin trong response_header) cho từng loại header_type tương ứng
def http_header(header_type):
    if header_type == '200':
        header = 'HTTP/1.1 200 OK\r\n'
    elif header_type == '404':
        header = 'HTTP/1.0 404 page not found\r\n'
    elif header_type == '401':
        header = 'HTTP/1.1 401 Unauthorized\r\n'
    return header

#Hàm trả về response_header tương ứng với từng loại content_type
def response_header(header_type, Content_type):
    message_header = http_header(header_type)
    message_header += f'Content-type: {Content_type}'
    message_header += '\r\n\r\n'
    message_header = message_header.encode()
    return message_header

#Hàm đọc nội dung file và chuyển data đã đọc về dưới dạng nhị phân (byte)
def read_file(file_url, header_type, Content_type):
    f = open(file_url, 'rb')
    f_data = response_header(header_type, Content_type)
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
        request_url = (request_line.split(' ')[1]).strip('/')

        #print(f'-Data: \n{data}')
        print(f'\n-Request line: {request_line}')
        print(f'-Request method: {request_method}')
        print(f'-Request url: {request_url}')
        
        # == 3. TẢI ĐƯỢC PAGE INDEX.HTML == 
        #Nếu method nhận được là GET: 
        if request_method == 'GET':
            #Với mỗi loại request_url ( loại file cần đọc), cần trả về các thông tin url (đường dẫn file); content_type và header_type tương ứng
            if request_url == '' or request_url == 'index.html':
                url = 'D:/Github/MangMayTinh/SocketProject/index.html' 
                Content_type = 'text/html'
                header_type = '200'
            elif request_url == 'css/style.css':
                url = 'D:/Github/MangMayTinh/SocketProject/' + request_url
                Content_type = 'text/css'
                header_type = '200'
            elif request_url == 'favicon.ico':
                url = 'D:/Github/MangMayTinh/SocketProject/' + request_url
                Content_type = 'image/x-icon'
                header_type = '200'
            elif(request_url.split('/')[0] == 'images'):
                url = 'D:/Github/MangMayTinh/SocketProject/' + request_url
                header_type = '200'
                Content_type = 'image/jpeg' 
            elif(request_url.split('/')[0] == 'avatars'): 
                url = 'D:/Github/MangMayTinh/SocketProject/' + request_url
                header_type = '200'
                Content_type = 'image/png' 
            else:
                # == 4. LỖI PAGE ==
                #Nếu Load Page Không Đúng Thì Trả Về 404.html
                header_type = '404'
                url = 'D:/Github/MangMayTinh/SocketProject/404.html'
                Content_type = 'text/html'
                print('* Error 404: File not found *')
            print("\n") 
            
        # == 4. ĐĂNG NHẬP ==
        #Nếu method nhận được là POST:
        
        
        #SendBackData (nhị phân) là dữ liệu đọc từ hàm read_file (bao gồm response_header và nội dung file đọc tương ứng)  
        sendBackData = read_file(url,header_type, Content_type)
        
        #Gửi nội dung data đã đọc lại cho client
        client.send(sendBackData)
         
        #Đóng Kết Nối Client
        client.close()
        break

# == 1. KẾT NỐI == 
#Cho Mở Kết Nối Server Để Lắng Nghe Kết Nối Từ Client
def start_server():
    SERVER.listen()
    while True:
        # == 6. MULTIPLE REQUESTS
        #Chấp nhận Kết Nối từ Client 
        conn, addr = SERVER.accept()
        
        # == 7. MULTIPLE CONNECTIONS ==
        #Thread dùng để xử lý nhiều connection cùng 1 lúc
        thread = threading.Thread(target= handle, args=(conn, addr))
        thread.start()
    
    
if __name__ == '__main__':
    start_server()