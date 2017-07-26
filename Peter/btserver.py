import asyncore
import logging
from bluetooth import *
from bthandler import BTClientHandler

logger = logging.getLogger(__name__)


class BTServer(asyncore.dispatcher):                      # 그냥 정의임
    """Asynchronous Bluetooth  Server"""

    def __init__(self, uuid, service_name, port=PORT_ANY):  # 이컨스트럭터가 3개의 변수 (62번 줄에서 내려옴)
        asyncore.dispatcher.__init__(self)

        self._cmds = {}                      # 아무것도

        if not is_valid_uuid(uuid):                          #아이디가 맞으면
            raise ValueError("uuid %s is not valid" % uuid)

        self.uuid = uuid
        self.service_name = service_name
        self.port = port

        # Create the server-side BT socket
        self.set_socket(BluetoothSocket(RFCOMM))      #소켓을 만들고 오브젝트를 넣는다.
        self.bind(("", self.port))            # 어떤 주소로
        self.listen(1)

        advertise_service(self.socket,
                          self.service_name,
                          service_id=self.uuid,
                          service_classes=[self.uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE]
                          )

        self.port = self.socket.getsockname()[1]
        logger.info("Waiting for connection on RFCOMM channel %d" % self.port)     # 로그인 기다린다
        print "Waiting for connection on RFCOMM channel %d" % self.port

    def handle_accept(self):                                      #누군가가 서버에 접근하면
        # This method is called when an incoming connection request from a client is accept.
        # Get the client-side BT socket
        pair = self.socket.accept()                                #클라이언트 소켓, 클라이언트 info

        if pair is not None:
            client_sock, client_addr = pair
            logger.info("Accepted connection from %s" % repr(client_addr[0]))     #인포 서버로 보내고
            print "Accepted connection from %s" % repr(client_addr[0])
            handler = BTClientHandler(socket=client_sock, server=self)                #중요 ? BTC뭐뭐 핸들러.py 만들고 비티시 뭐 핸들러에서 가져와서, 그 파이선 코드가서

    def handle_connect(self):
        # This method is called when the connection is established.
        pass

    def handle_close(self):
        self.close()

if __name__ == '__main__':                                  # 그래서 역서 시작. python btserver.py 하면 펑션네임이 main. main 뻥션 네임이 main 이면 작동되고 아니면 아무것도 안됨.
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"       # 각각의 서버마다 유니크 아이디를가진다
    service_name = "AsynchronousBTServer"                 #서버네임

    server = BTServer(uuid, service_name)                    # uuid가 btserver은 object 이 오브젝트는 12번줄에 ?
    asyncore.loop()                                          # while 루프랑 비슷
