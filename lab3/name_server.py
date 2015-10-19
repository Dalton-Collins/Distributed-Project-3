"""
    Name server behaves as follows:
        Accepts requests from clients to register them,
        unregister them, or return a list of clients
        registered with a particular object type.

        There are four data elments associated to each client:
            address        hostname and portnumber of the client machine
            type        String indicating object type of the client object
            id            [unspecified] identifier for the client object
            hash        [unspecified] hashcode for the client object


Having both id and hash seems kind of redundant.
    -W
"""

# Use same request class as peer
import sys
sys.path.append("../modules")
from Common.orb import Request
from Common.nameServiceLocation import name_service_address

import threading
import socket

# Skeleton object for the name server
class NSListener(threading.Thread):

    def __init__(self,nameService,address):
        threading.Thread.__init__(self)

        self.nameService = nameService

        self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenSocket.bind(address)
        self.listenSocket.listen(0)

    def run(self):
        while True:
            try:
                conn, addr = self.listenSocket.accept()
                req = Request(self.nameService, conn, addr)
                print("Serving a request from {0}".format(addr))
                req.start()
            except socket.error:
                print(socket.error)
                continue
            finally:
                pass

class NameService:

    def __init__(self):
        self.peers = dict()
        self.count = 0

        # Use the predefined name service address
        self.address = name_service_address

        self.skeleton = NSListener(self, self.address)

    def start(self):
        self.skeleton.start()

    def register(self, type, address):
        print((type, address))
        try:
            id = self.count
            self.count += 1

            hashcode = hash(str(list))

            key = str((id, hashcode))

            if type in self.peers:
                self.peers[type][key] = (id, address)
            else:
                self.peers[type] = {key: address}
            print (id, str(hashcode))
            return (id, str(hashcode))
        except Exception as e:
            print(e)
        finally:
            pass

    def unregister(self, id, type, hashcode):
        key = str((id, hashcode))

        try:
            del self.peers[type][key]

            # Remove the sub-dict for this object type
            # if there are no longer any registered peers
            if not len(self.peers[type]):
                del self.peers[type]

            # if peers[type][key] does not exit, a KeyError will be
            # caught by the request object and sent back to client.
        finally:
            pass

    def require_all(self, type):
        if type in self.peers:
            return self.peers[type].values()
        else:
            # If there are no matches for this object type, return an empty list
            return []

try:
    ns = NameService()
    ns.start()
except Exception as e:
    print(e)
finally:
    pass
