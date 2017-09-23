import cv2
import numpy as np

# 라이브러리 등록

font = cv2.FONT_HERSHEY_SIMPLEX


# 폰트 등록

def faceDetect():
    face_cascade = cv2.CascadeClassifier('C:\\Program Files\\OpenCV3.3\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
    upper_cascade = cv2.CascadeClassifier('C:\\Program Files\\OpenCV3.3\\opencv\\build\\etc\\haarcascades\\haarcascade_upperbody.xml')
    # 영상에서 인식할 소스 등록
    try:
        cap = cv2.VideoCapture(0)
        print('카메라 로딩 성공')
    # 웹캠 활성화시키는 코드

    except:
        print('카메라 로딩 실패')
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
                    cv2.rectangle(frame, (faceX, faceY), (faceX + face_width, faceY + face_height),
                                  (255, 0, 0), 3, 4, 0)
                    cv2.rectangle(frame, (upperX, upperY), (upperX + upper_width, upperY + upper_height),
                                  (255, 0, 0), 3, 4, 0)

                    cv2.putText(frame, 'Detected Face', (faceX - 5, faceY - 5), font, 0.9, (255, 255, 0), 2)
                    img_trim = frame[upperY:upperY+ upper_height, upperX:upperX+upper_width]
                    cv2.imwrite('SSong.jpg', img_trim)

        # 얼굴을 인식하는 사각형에 대한 소스, 텍스트 소스

        cv2.imshow('frame', frame)
        # 영상을 출력하는 소스

        if cv2.waitKey(1) == 255:
            break;
    cap.release()
    cv2.destroyAllWindows()


# space를 누르면 실행 종료되는 코드

faceDetect()