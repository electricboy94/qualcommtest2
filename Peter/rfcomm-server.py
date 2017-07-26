# file: rfcomm-server.py

# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *     # 아무라이브러리 (블루투스 라이브러리에잇는걸 다 땡겨온다)

server_sock = BluetoothSocket(RFCOMM)    # 일종의 시리얼 포트  블루투스 소켓 오브젝트 RFcomm 으로부터 create bluetooth socket object from rfcomm ,RFCOM 값을 받아서 BL~~ 실행시키는데, 실행시키는 이름이 서버속
server_sock.bind(("", PORT_ANY))         # 어느 포켓이나 가능
server_sock.listen(1)                    #1 나의 클라이언트만 서버에 접근가능

port = server_sock.getsockname()[1]      # 아무포켓이나 가능하다했으니까 그중에 내가들을 포트 정하는것

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"     # 유니크넘버

advertise_service(server_sock,        # 어떤소켓 할지 정하는거
                  "SampleServer",   # 서버네임
                  service_id=uuid,    #서버아이디
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  protocols = [ OBEX_UUID ]                ## 온라인 되야 advertise 할수잇다 ?
                  )

print "Waiting for connection on RFCOMM channel %d" % port  #일단 블루투스 연결하면

client_sock, client_info = server_sock.accept()     # 프로그램이 컨넥션을 기다리려고 스톱한다.
print "Accepted connection from ", client_info  # 컨넥트 되면 이 라인으로 옮겨지고, 소켓으로가고, 클라이언트로가고, 클라이언트로 보내고싶으면 그 소캣으로 보내야한다

try:
    while True:
        data = client_sock.recv(1024)   # 버퍼를 열어놓고 내폰에 받을 메세지를 기다린다 (1024 byte 버퍼사이즈 저장할수있따는것을 의미함)
        if len(data) == 0:              # 0되면 멈추고
            break
        print "received [%s]" % data     # 0 가 아니면 프린트됨
        sent = client_sock.send("received [%s]\n" % data) # 중요 뭔가를 폰으로 되돌려보낸다.  유드보드에서 폰으로 뭔가를 돌려보낼 때 client send 하고 뒤에 메세지적으면됨
        if sent == 0:                        # 만약에 너무 크게보내거다 그러면 신호 잊음 1000 보내고ㅅ피엇는데 500만 가면 에러
            raise RuntimeError("socket connection broken")   # 끊겻다고 메세지 뜸
except IOError:
    pass

print "disconnected"             # 프린트

client_sock.close()
server_sock.close()
print "all done"
