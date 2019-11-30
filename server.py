import pygame, math
import sys
import time
import socket, threading

# 서버의 설정값을 저장
myip = '127.0.0.1'
myport = 50000
address = (myip, myport)

# 서버를 연다.
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(address)
server_sock.listen()
print('Start Chat - Server')

# 접속한 클라이언트들을 저장할 공간
client_list = []
client_id = []
game_start_flag = False
player1,player2=None,None
p_1_event,p_2_event=None,None

# 서버로 부터 메시지를 받는 함수 | Thread 활용
def receive(client_sock):
    global client_list,player1,p_1_event,player2,p_2_event  # 받은 메시지를 다른 클라이언트들에게 전송하고자 변수를 가져온다.
    thread_send = threading.Thread(target = send, args = (client_sock,))
    thread_send.start()
    while True:
        # 클라이언트로부터 데이터를 받는다.
        try:
            data = client_sock.recv(1024)
        except ConnectionError:
            print("{}와 연결이 끊겼습니다. #code1".format(client_sock.fileno()))
            break

        if not data:
            print("{}이 연결 종료 요청을 합니다. #code0".format(client_sock.fileno()))
            client_sock.send(bytes("서버에서 클라이언트 정보를 삭제하는 중입니다.", 'utf-8'))
            break

        if client_sock==player1:
            p_1_event = data.decode('UTF-8')
        else:
            p_2_event = data.decode('UTF-8')

    client_id.remove(client_sock.fileno())
    client_list.remove(client_sock)
    print("현재 연결된 사용자: {}\n".format(client_id), end='')
    # 삭제 후 sock 닫기
    client_sock.close()
    print("클라이언트 소켓을 정상적으로 닫았습니다.")
    print('#----------------------------#')
    return 0

def send(client_sock):
    global p_1_event,p_2_event
    print('a')
    while True:
        client_sock.send(bytes(p_1_event,'utf-8'))
        client_sock.send(bytes('and','utf-8'))
        client_sock.send(bytes(p_2_event,'utf-8'))

def game_start():
    global client_list
    player1=client_list[0]
    player2=client_list[1]
    for sock in client_list:
        sock.send(bytes('game start', 'UTF-8'))
        thread_recv = threading.Thread(target=receive, args=(sock,))
        thread_recv.start()

    # 연결 수립용 함수 | Thread 활용
def connection():
    global client_list
    global client_id

    while True:
        # 클라이언트들이 접속하기를 기다렸다가, 연결을 수립함.
        client_sock, client_addr = server_sock.accept()

        if len(client_list)>=2:
            client_sock.send(bytes('이미 2명이 꽉 찼습니다.','utf-8'))
            client_sock.close()

        # 연결된 정보를 가져와서 list에 저장함.
        client_list.append(client_sock)
        client_id.append(client_sock.fileno())
        if len(client_list)== 2:
            game_start()

        print("{}가 접속하였습니다.".format(client_sock.fileno()))
        print("{}가 접속하였습니다.".format(client_addr))
        print("현재 연결된 사용자: {}\n".format(client_list))

thread_server = threading.Thread(target=connection, args=())
thread_server.start()

print("============== Chat Server ==============")

thread_server.join()
server_sock.close()