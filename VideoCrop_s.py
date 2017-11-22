#!/usr/bin/env python3

pre_name = 'NoNo'

def VideoCrop():
    import cv2
    import numpy as np
    import os
    font = cv2.FONT_HERSHEY_SIMPLEX
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    upper_cascade = cv2.CascadeClassifier('./haarcascade_upperbody.xml')
    eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')
    videodir = './'
#    videoName= input("Enter the video name: ")
    videoName = "Song3.mp4"
    videoName = videodir+videoName

    print("@@@@@@@!")
    try:
        cap = cv2.VideoCapture(videoName)
        print('Camera loading complete')
    except:
        print('Camera loading fail')
        return
    print("@@@@@@@@@2")
    targetName = "sample"
    absroute = "/root/openface/VideoCrop/"
    absroute += targetName
    if not os.path.isdir(absroute):
        os.mkdir(absroute)
    ## count = 1
    facecnt = 1
    uppercnt = 1
    eyecnt = 1
    print("!@@@@@@@@")
    cv2.namedWindow('Detect')
    print("@@dfdfd")
    ## fileName = "./" + targetName + "/" + targetName
    fileName = "./" + targetName
 
    print("@@@@@@@@@3")
    while True:
        ret, frame = cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 2, 0, (30, 30))
        uppers = upper_cascade.detectMultiScale(gray, 1.3, 2, 0, (30,30))
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 2, 0, (30,30))

        flag = 0;
        for (faceX, faceY, face_width, face_height) in faces:
            for(upperX, upperY, upper_width, upper_height) in uppers:
                if(upperX < faceX and upperX + upper_width > faceX + face_width and
                            upperY < faceY and upperY + upper_height > faceY + face_height):
                    flag = 1
                    img_trim = frame[upperY:upperY + upper_height, upperX:upperX + upper_width]
                    ImageName = fileName + "_upper/" + targetName + str(uppercnt) + ".jpg"
                    # cv2.imwrite(ImageName, img_trim)
                    cv2.imwrite(absroute + "/" + str(uppercnt) + ".jpg", img_trim)
                    uppercnt = uppercnt+1
                    compare(absroute + "/" + str(uppercnt) + ".jpg")
                    break

            if( flag == 1):
                break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 255:

            break;
    cap.release()
    cv2.destroyAllWindows()
def Compare(name):
    global pre_name
   # print (a)
  #  dirname = '/root/openface/compare/'
  #  name = ''
  #  dirname += a
   # print ('dirname = ',dirname)
    proc = subprocess.Popen(['/root/openface/demos/classifier2.py', 
        'infer', '/root/openface/generated-embeddings/classifier.pkl', 
        name], 
        stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE
        )

    out, err = proc.communicate()
   # print ('out = ',out)
    lists = out.split()
   # print('lists = ',lists)

   # print('pre_name = ',pre_name,'lists[4] = ',lists[4])
    if pre_name != lists[4]:
        print('@@@result = ',lists[4], lists[6], dirname)
    pre_name=lists[4]

   # print('\n\n')
    return lists[4], lists[6], dirname

if __name__ == '__main__':
    VideoCrop()
