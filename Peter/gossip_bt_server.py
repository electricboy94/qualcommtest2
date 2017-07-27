import asyncore

from btserver import BTServer
from bterror import BTError
from random import uniform
from threading import Thread
from time import sleep, time

if __name__ == '__main__':
    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "GossipBTServer"
    server = BTServer(uuid, service_name)

    # Create the server thread and run it
    server_thread = Thread(target=asyncore.loop, name="Gossip BT Server Thread")
    server_thread.daemon = True                          #  계속 진행된다 컨트롤 씨 하기전까지는
    server_thread.start()                                #

    while True:
        for client_handler in server.active_client_handlers.copy():         # 카피없으면 클라이언트가 컨넥션 없으면 에러뜬다.    클라이언트 수만큼 스레드 복사 !
            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"
            msg = "realtime, %d, %f, %f, %f, %f, %f, %f\n" % \                  # csv 메세지
                  (int(time()),         # epoch time                           # 리얼타임
                   uniform(20, 30),     # random temperature                   # 값
                   uniform(40, 50),     # random SN1 value
                   uniform(60, 70),     # random SN2 value
                   uniform(80, 90),     # random SN3 value
                   uniform(100, 110),   # random SN4 value
                   uniform(120, 130))   # random PM25 value

            try:
                client_handler.send(msg)
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 3 seconds
        sleep(3)
