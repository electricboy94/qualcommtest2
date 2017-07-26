import asyncore
import logging
from bterror import BTError

logger = logging.getLogger(__name__)


class BTClientHandler(asyncore.dispatcher_with_send):
    """BT handler for client-side socket"""

    def __init__(self, socket, server):
        asyncore.dispatcher_with_send.__init__(self, socket)
        self._server = server
        self._data = ""

    def handle_read(self):                              # 안드로이드가 클라이언트 소켓으로 보내면 이 문장이 trigger 된다
        try:
            data = self.recv(1024)
            if not data:
                return

            lf_char_index = data.find('\n')             #받으면 줄바꿈? 뭐지 물어보기

            if lf_char_index == -1:
                # No new line character in data, so we append all.
                self._data += data
            else:
                # We see a new line character in data, so append rest and handle.
                self._data += data[:lf_char_index]
                print "received [%s]" % self._data

                self.send(self._data + '\n')           # 완료되면 샌드백, 완료안되면 계속듣는다 ?

                # Clear the buffer
                self._data = ""
        except Exception as e:
            BTError.print_error(handler=self, error=BTError.ERR_READ, error_message=repr(e))
            self._data = ""
            self.close()

    def handle_close(self):                    # 뭔가 잘못되면 or 클로스 컨넥션 , 핸들클로스로가서  .. ?
        # flush the buffer
        while self.writable():
            self.handle_write()
        self.close()
