#!/usr/bin/env python2
import os
import sys
sys.path.insert(0,"/home/ubuntu/OpenFace/openface/NFG")
import NFG
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
import cv2
import imagehash
import json
import numpy as np
import os
import StringIO
import urllib
import base64
import signal
import threading
import base64
import openface

tls_crt = os.path.join(fileDir, 'tls', 'server.crt')
tls_key = os.path.join(fileDir, 'tls', 'server.key')

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=9000,
                    help='WebSocket Port')

args = parser.parse_args()
"""
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
def faceDetect(parent):
	try:
		capture = cv2.VideoCapture(0)
		print('Success')
	except:
		print('Failure')
		return
	#while True:
	ret, frame = capture.read()
	ret, temp = cv2.imencode('.png', frame)
	data = base64.encodestring(temp)
	length = len(data)
	message = {
		'type' : 'VIDEO',
		'length' : length,
		'data' : data
	}
	parent.sendMessage(json.dumps(message))
	print(length, data)
"""
class OpenFaceServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(OpenFaceServerProtocol, self).__init__()
        self.images = {}
        self.training = True
        self.people = []
        self.svm = None
#        self.t = threading.Thread(target=faceDetect, args=(self,))
#        self.t.start()
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
        if msg['type'] == "ALL_STATE":
            self.loadState(msg['images'], msg['training'], msg['people'])
        elif msg['type'] == 'COMPARE':
            print("COMPARE START")
            self.Compare();
        elif msg['type'] == "TRAIN":
            print("TRAIN START")
            NFG.Train()
            msg = {
                    "type" : "TRAIN_RETURN"
                    };
            self.sendMessage(json.dumps(msg))
        else:
            print("Warning: Unknown message type: {}".format(msg['type']))
    def Compare(self):
        name, confidence, path = NFG.Compare()
        msg = {
                "type" : "COMPARE_RETURN",
                "name" : name,
                "confidence" : confidence,
                "path" : path
                }
        self.sendMessage(json.dumps(msg))
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
