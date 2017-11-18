#!/usr/bin/env python2
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

import openface

tls_crt = os.path.join(fileDir, 'tls', 'server.crt')
tls_key = os.path.join(fileDir, 'tls', 'server.key')

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=9898,
                    help='WebSocket Port')

args = parser.parse_args()
"""
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
def faceDetect(parent):
    cnt = 0
    
    face_cascade = cv2.CascadeClassifier('/home/ubuntu/OpenFace/openface/demos/web/haarcascade_frontalface_default.xml')
    upper_cascade = cv2.CascadeClassifier('/home/ubuntu/OpenFace/openface/demos/web/haarcascade_upperbody.xml')
    try:
        cap = cv2.VideoCapture(2)
        print('Success')

    except:
        print('Failure')
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 2, 0, (30, 30))
        uppers = upper_cascade.detectMultiScale(gray, 1.3, 2, 0, (30,30))
        for (faceX, faceY, face_width, face_height) in faces:
            for(upperX, upperY, upper_width, upper_height) in uppers:
                if(upperX < faceX and upperX + upper_width > faceX + face_width and
                            upperY < faceY and upperY + upper_height > faceY + face_height):
                    img_trim = frame[upperY:upperY+ upper_height, upperX:upperX+upper_width]
                    cv2.imwrite('/home/ubuntu/dataset/detect' + str(cnt // 10) + '.png', img_trim)
                    cnt+=1
                    
        if(cnt % 10 == 1):
            parent.Compare()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 255:
            break;
    
    cap.release()
    cv2.destroyAllWindows()
"""
class OpenFaceServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(OpenFaceServerProtocol, self).__init__()
        self.images = {}
        self.training = True
        self.people = []
        self.svm = None
	print("================MOVIESOCEKT================")
     #   self.t = threading.Thread(target=faceDetect, args=(self,))
     #   self.t.start()
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

