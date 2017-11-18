#!/usr/bin/env python2
#
# Copyright 2015-2016 Carnegie Mellon University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, "..", ".."))

import txaio
txaio.use_twisted()

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.internet import task, defer
from twisted.internet.ssl import DefaultOpenSSLContextFactory

from twisted.python import log

import argparse
import json
from PIL import Image
import os
import StringIO
import urllib
import base64
import signal
import threading

# For TLS connections
tls_crt = os.path.join(fileDir, 'tls', 'server.crt')
tls_key = os.path.join(fileDir, 'tls', 'server.key')

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=9000,
                    help='WebSocket Port')

args = parser.parse_args()

class OpenFaceServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(OpenFaceServerProtocol, self).__init__()
        self.images = {}
        self.training = True
        self.people = []
        self.svm = None
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.training = True

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        raw = payload.decode('utf8')
        msg = json.loads(raw)
        print("Received {} message of length {}.".format(
            msg['type'], len(raw)))
        print("Warning: Unknown message type: {}".format(msg['type']))
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

def main(reactor):
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory()
    factory.protocol = OpenFaceServerProtocol
    ctx_factory = DefaultOpenSSLContextFactory(tls_key, tls_crt)
    reactor.listenSSL(args.port, factory, ctx_factory)
    return defer.Deferred()

if __name__ == '__main__':
    task.react(main)
