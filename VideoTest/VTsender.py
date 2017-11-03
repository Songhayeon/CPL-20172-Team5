import socket
import cv2
import numpy
import flask

#연결할 서버(수신단)의 ip주소와 port번호
TCP_IP = 'localhost'
TCP_PORT = 5002

#송신을 위한 socket 준비
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

#OpenCV를 이용해서 webcam으로 부터 이미지 추출
try:
    # cap = cv2.VideoCapture(0)
    # 0은 현재 연결된 카메라 자원
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    print('Camera loading complete')
# 웹캠 활성화시키는 코드
except:
    print('Camera loading fail')

while 1:
    ret, frame = capture.read()
    cv2.imshow('CLIENT', frame)

    #추출한 이미지를 String 형태로 변환(인코딩)시키는 과정
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    #stringData = stringData.encode('utf-8')
    length = len(stringData)
    length_data = str(length).ljust(16)
    length_data = length_data.encode('utf-8')
    print(str(len(length_data)) + " " + str(length_data))
    #String 형태로 변환한 이미지를 socket을 통해서 전송
    sock.send( length_data)

    sock.send( stringData)

    #다시 이미지로 디코딩해서 화면에 출력. 그리고 종료
    decimg=cv2.imdecode(data,1)
    #cv2.imshow('CLIENT', decimg)

capture.release()
cv2.destroyAllWindows()

sock.close()