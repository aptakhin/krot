from contextlib import contextmanager
import io
import json
import socket
import ssl
from typing import Any
import httpx
import pytest
import os
import json as json_impl

import select

import requests
# from urllib3.connection import match_hostname as urllib3_match_hostname
# from urllib3.util.ssl_ import ssl_wrap_socket as urllib3_ssl_wrap_socket
# from urllib3.util.ssl_ import wrap_socket as urllib3_wrap_socket



true_socket = socket.socket
true_create_connection = socket.create_connection
true_gethostbyname = socket.gethostbyname
true_gethostname = socket.gethostname
true_getaddrinfo = socket.getaddrinfo
true_socketpair = socket.socketpair
true_ssl_wrap_socket = ssl.wrap_socket
true_ssl_socket = ssl.SSLSocket
true_ssl_context = ssl.SSLContext
true_inet_pton = socket.inet_pton
# true_urllib3_wrap_socket = urllib3_wrap_socket
# true_urllib3_ssl_wrap_socket = urllib3_ssl_wrap_socket
# true_urllib3_match_hostname = urllib3_match_hostname

from socket import _GLOBAL_DEFAULT_TIMEOUT, SOCK_STREAM

import _socket

class MocketSocketCore(io.BytesIO):
    def write(self, content):
        super().write(content)

        # if Mocket.r_fd and Mocket.w_fd:
            # os.write(Mocket.w_fd, content)

def socketpair(*args, **kwargs):
    """Returns a real socketpair() used by asyncio loop for supporting calls made by fastapi and similar services."""
    import _socket

    return _socket.socketpair(*args, **kwargs)


class KrotSocket:
    timeout = None
    _fd = None
    family = None
    type = None
    proto = None
    _host = None
    _port = None
    _address = None
    cipher = lambda s: ('ADH', 'AES256', 'SHA')
    compression = lambda _: ssl.OP_NO_COMPRESSION
    _mode = None
    _bufsize = None
    _secure_socket = False

    def __init__(
        self,
        context: 'Context',
        family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, *args, **kwargs
    ):
        self.true_socket = true_socket(family, type, proto)
        self._buflen = 65536
        self._entry = None
        self.family = int(family)
        self.type = int(type)
        self.proto = int(proto)
        self._truesocket_recording_dir = None
        self.kwargs = kwargs
        self._context = context

    def __str__(self):
        return '({})(family={} type={} protocol={})'.format(
            self.__class__.__name__, self.family, self.type, self.proto
        )

    # def __enter__(self):
    #     return self

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.close()

    @property
    def fd(self):
        if self._fd is None:
            self._fd = MocketSocketCore()
        return self._fd

    def gettimeout(self):
        return self.timeout

    def setsockopt(self, family, type, proto):
        self.family = family
        self.type = type
        self.proto = proto

        if self.true_socket:
            self.true_socket.setsockopt(family, type, proto)

    def settimeout(self, timeout):
        self.timeout = timeout

    @staticmethod
    def getsockopt(level, optname, buflen=None):
        return socket.SOCK_STREAM

    # def do_handshake(self):
    #     pass

    def getpeername(self):
        return self._address

    def setblocking(self, block):
        self.settimeout(None) if block else self.settimeout(0.0)

    def getsockname(self):
        return socket.gethostbyname(self._address[0]), self._address[1]

    # def getpeercert(self, *args, **kwargs):
    #     if not (self._host and self._port):
    #         self._address = self._host, self._port = Mocket._address

    #     now = datetime.now()
    #     shift = now + timedelta(days=30 * 12)
    #     return {
    #         "notAfter": shift.strftime("%b %d %H:%M:%S GMT"),
    #         "subjectAltName": (
    #             ("DNS", "*.%s" % self._host),
    #             ("DNS", self._host),
    #             ("DNS", "*"),
    #         ),
    #         "subject": (
    #             (("organizationName", "*.%s" % self._host),),
    #             (("organizationalUnitName", "Domain Control Validated"),),
    #             (("commonName", "*.%s" % self._host),),
    #         ),
    #     }

    # def unwrap(self):
    #     return self

    # def write(self, data):
    #     return self.send(encode_to_bytes(data))

    @staticmethod
    def fileno():
        r_fd, w_fd = os.pipe()
        return r_fd

    def connect(self, address):
        self._address = self._host, self._port = address

    def makefile(self, mode='r', bufsize=-1):
        self._mode = mode
        self._bufsize = bufsize
        return self.fd

    # def get_entry(self, data):
    #     return Mocket.get_entry(self._host, self._port, data)

    def sendall(self, data, entry=None, *args, **kwargs):
        # if entry is None:
        #     entry = self.get_entry(data)

        # if entry:
        #     consume_response = entry.collect(data)
        #     if consume_response is not False:
        #         response = entry.get_response()
        #     else:
        #         response = None
        # else:
        response = self.true_sendall(data, *args, **kwargs)

        if response is not None:
            self.fd.seek(0)
            self.fd.write(response)
            self.fd.truncate()
            self.fd.seek(0)

    # def read(self, buffersize):
    #     return self.fd.read(buffersize)

    # def recv_into(self, buffer, buffersize=None, flags=None):
    #     return buffer.write(self.read(buffersize))

    # def recv(self, buffersize, flags=None):
    #     if Mocket.r_fd and Mocket.w_fd:
    #         return os.read(Mocket.r_fd, buffersize)
    #     data = self.read(buffersize)
    #     if data:
    #         return data
    #     # used by Redis mock
    #     exc = BlockingIOError()
    #     exc.errno = errno.EWOULDBLOCK
    #     exc.args = (0,)
    #     raise exc

    def true_sendall(self, data, *args, **kwargs):
        # if MocketMode().STRICT:
        #     raise StrictMocketException("Mocket tried to use the real `socket` module.")

        # req = decode_from_bytes(data)
        # # make request unique again
        # req_signature = _hash_request(hasher, req)
        # # port should be always a string
        # port = text_type(self._port)

        # # prepare responses dictionary
        # responses = {}

        # if Mocket.get_truesocket_recording_dir():
        #     path = os.path.join(
        #         Mocket.get_truesocket_recording_dir(), Mocket.get_namespace() + ".json"
        #     )
        #     # check if there's already a recorded session dumped to a JSON file
        #     try:
        #         with io.open(path) as f:
        #             responses = json.load(f)
        #     # if not, create a new dictionary
        #     except (FileNotFoundError, JSONDecodeError):
        #         pass

        # try:
        #     try:
        #         response_dict = responses[self._host][port][req_signature]
        #     except KeyError:
        #         if hasher is not hashlib.md5:
        #             # Fallback for backwards compatibility
        #             req_signature = _hash_request(hashlib.md5, req)
        #             response_dict = responses[self._host][port][req_signature]
        #         else:
        #             raise
        # except KeyError:
        #     # preventing next KeyError exceptions
        #     responses.setdefault(self._host, {})
        #     responses[self._host].setdefault(port, {})
        #     responses[self._host][port].setdefault(req_signature, {})
        #     response_dict = responses[self._host][port][req_signature]

        # try to get the response from the dictionary
        # try:
        #     encoded_response = hexload(response_dict["response"])
        # # if not available, call the real sendall
        # except KeyError:
        host, port = self._address
        host = true_gethostbyname(host)

        # if isinstance(self.true_socket, true_socket) and self._secure_socket:
        #     self.true_socket = true_urllib3_ssl_wrap_socket(
        #         self.true_socket,
        #         **self.kwargs,
        #     )

        data = b'GET /status/200 HTTP/1.1\r\nHost: httpbin.org\r\nUser-Agent: python-requests/2.28.2\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
        print(f'X, {host=}, {port=}, {data=}, {args=}, {kwargs=}')

        try:
            self.true_socket.connect((host, port))
        except (OSError, socket.error, ValueError):
            # already connected
            pass
        self.true_socket.sendall(data, *args, **kwargs)
        encoded_response = b''
        # https://github.com/kennethreitz/requests/blob/master/tests/testserver/server.py#L13
        while True:
            if (
                not select.select([self.true_socket], [], [], 0.1)[0]
                and encoded_response
            ):
                break
            recv = self.true_socket.recv(self._buflen)

            if not recv and encoded_response:
                break
            encoded_response += recv

            # # dump the resulting dictionary to a JSON file
            # if Mocket.get_truesocket_recording_dir():

            #     # update the dictionary with request and response lines
            #     response_dict["request"] = req
            #     response_dict["response"] = hexdump(encoded_response)

            #     with io.open(path, mode="w") as f:
            #         f.write(
            #             decode_from_bytes(
            #                 json.dumps(responses, indent=4, sort_keys=True)
            #             )
            #         )
        print('  return', encoded_response)
        respo = self._context._responses[0]

        ln = str(len(respo)).encode('utf-8')
        print('  rrxx', respo, type(respo))
        print('  xx', ln)
        respo_all = b'HTTP/1.1 200 OK\r\nDate: Fri, 07 Apr 2023 16:01:04 GMT\r\nContent-Type: text/json; charset=utf-8\r\nContent-Length: ' + ln + b'\r\nConnection: keep-alive\r\nServer: gunicorn/19.9.0\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Credentials: true\r\n\r\n' + respo
        print('  ret', respo_all)
        return respo_all

        # response back to .sendall() which writes it to the Mocket socket and flush the BytesIO
        return encoded_response

    def send(self, data, *args, **kwargs):  # pragma: no cover
        # entry = self.get_entry(data)
        # if not entry or (entry and self._entry != entry):
        self.sendall(data, entry=None, *args, **kwargs)
        # else:
        #     req = Mocket.last_request()
        #     if hasattr(req, "add_data"):
        #         req.add_data(data)
        # self._entry = entry
        return len(data)

    def close(self):
        if self.true_socket and not self.true_socket._closed:
            self.true_socket.close()
        self._fd = None

    def __getattr__(self, name):
        """Do nothing catchall function, for methods like close() and shutdown()"""

        def do_nothing(*args, **kwargs):
            pass

        return do_nothing


def create_connection(address, timeout=None, source_address=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    if timeout:
        s.settimeout(timeout)
    s.connect(address)
    return s


class Context:
    def __init__(self) -> None:
        self._responses = []

    def start(self) -> None:
        socket.create_connection = create_connection

        socket.socketpair = socketpair

        def socket_impl(family=None, type=SOCK_STREAM, proto=0):
            # assert False
            return KrotSocket(context=self)
        socket.socket = socket_impl

    def dispose(self) -> None:
        pass

    def add_response(self, json: dict[str, Any]) -> None:
        self._responses.append(json_impl.dumps(json).encode('utf-8'))


@contextmanager
def mock():
    context = Context()
    context.start()

    yield context

    context.dispose()


def test_requests():
    with mock() as context:
        context.add_response(json={'hello': 'world'})

        response = requests.get('http://httpbin.org/status/200')
        assert response.json() == {'hello': 'world'}


@pytest.mark.skip
@pytest.mark.asyncio
async def test_it():
    with mock() as context:
        context.add_response(json={})

        async with httpx.AsyncClient() as client:
            response = await client.get('http://httpbin.org/status/200')
            assert response.json() == {}
