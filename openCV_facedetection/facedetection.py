import cv2
import sys
import numpy as np
import os

font = cv2.FONT_HERSHEY_SIMPLEX

def faceDetect():
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    upper_cascade = cv2.CascadeClassifier('./haarcascade_upperbody.xml')
    eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')

    videoName= input("Enter the video name: ")
    # 영상에서 인식할 소스 등록
    try:
        # cap = cv2.VideoCapture(0)
        # 0은 현재 연결된 카메라 자원
        cap = cv2.VideoCapture(videoName)
        print('Camera loading complete')
    # 웹캠 활성화시키는 코드
    except:
        print('Camera loading fail')
        return

    #Target이름
    targetName = input("Enter the target name:")

    if not os.path.isdir("./" + targetName + "_face"):
        os.mkdir("./" + targetName + "_face")

    if not os.path.isdir("./" + targetName + "_upper"):
        os.mkdir("./" + targetName + "_upper")

    if not os.path.isdir("./" + targetName + "_eye"):
        os.mkdir("./" + targetName + "_eye")


    ## count = 1
    facecnt = 1
    uppercnt = 1
    eyecnt = 1
    cv2.namedWindow('Detect')
    ## fileName = "./" + targetName + "/" + targetName
    fileName = "./" + targetName
    while True:
        ret, frame = cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 2, 0, (30, 30))
        uppers = upper_cascade.detectMultiScale(gray, 1.3, 2, 0, (30,30))
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 2, 0, (30,30))


        for (faceX, faceY, face_width, face_height) in faces:
            img_trim = frame[faceY:faceY+ face_height, faceX:faceX+face_width]
            ImageName = fileName + "_face/" + targetName + str(facecnt) + ".jpg"
            cv2.imwrite(ImageName, img_trim)
            ##count = count + 1
            facecnt = facecnt + 1

        flag = 0;
        for (faceX, faceY, face_width, face_height) in faces:
            for(upperX, upperY, upper_width, upper_height) in uppers:

                if(upperX < faceX and upperX + upper_width > faceX + face_width and
                            upperY < faceY and upperY + upper_height > faceY + face_height):
                    flag = 1
                    img_trim = frame[upperY:upperY + upper_height, upperX:upperX + upper_width]
                    ## ImageName = fileName + str(uppercnt) + ".jpg"
                    ImageName = fileName + "_upper/" + targetName + str(uppercnt) + ".jpg"
                    cv2.imwrite(ImageName, img_trim)
                    ##count = count + 1
                    uppercnt = uppercnt + 1
                    '''
                    cv2.rectangle(frame, (faceX, faceY), (faceX + face_width, faceY + face_height),
                                  (255, 0, 0), 3, 4, 0)
                    cv2.rectangle(frame, (upperX, upperY), (upperX + upper_width, upperY + upper_height),
                                  (255, 0, 0), 3, 4, 0)

                    cv2.putText(frame, 'Detected Face', (faceX - 5, faceY - 5), font, 0.9, (255, 255, 0), 2)
                    '''
                    break
            if( flag == 1):
                break

        # 얼굴을 인식하는 사각형에 대한 소스, 텍스트 소스

        for (faceX, faceY, face_width, face_height) in faces:
            for (eyeX, eyeY, eye_width, eye_height) in eyes:

                if (eyeX > faceX and eyeX + eye_width < faceX + face_width and
                            eyeY > faceY and eyeY + eye_height < faceY + face_height):

                    img_trim = frame[faceY: faceY+face_height, faceX: faceX + face_width]
                    ImageName = fileName + "_eye/" + targetName + str(eyecnt) + ".jpg"
                    cv2.imwrite(ImageName, img_trim)
                    ## count = count + 1
                    eyecnt = eyecnt + 1

        cv2.imshow('frame', frame)
        # 영상을 출력하는 소스
        if cv2.waitKey(1) == 255:
            break;

    cap.release()
    cv2.destroyAllWindows()

# space를 누르면 실행 종료되는 코드

faceDetect()