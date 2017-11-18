#!/usr/bin/env python3
import subprocess
import sys
sys.path.insert(0, "/home/ubuntu/OpenFace/VideoDetection/")
import facedetection as detect

def Train():
    proc = subprocess.Popen(['/home/ubuntu/OpenFace/openface/util/align-dlib.py', '/home/ubuntu/dataset/data', 
        'align', 'outerEyesAndNose',
        '/home/ubuntu/dataset/align/', 
        '--size', '96'],
        stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
    out, err = proc.communicate()
    print(out.decode('UTF-8'))
    print('ALIGN DONE')
    proc = subprocess.Popen(['/home/ubuntu/OpenFace/openface/batch-represent/main.lua', 
        '-outDir', '/home/ubuntu/dataset/embedding/', 
        '-data', '/home/ubuntu/dataset/align/'], 
        stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )

    out, err = proc.communicate()
    print(out.decode('UTF-8'))
    print('EMBEDDING DONE')
    proc = subprocess.Popen(['rm', '/home/ubuntu/dataset/align/cache.t7'])

    out, err = proc.communicate()
    proc = subprocess.Popen(['/home/ubuntu/OpenFace/openface/demos/classifier.py', 'train', '/home/ubuntu/dataset/embedding/'],
                stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    
    out, err = proc.communicate()
    print ("==TRAIN DONE==")


def Compare():
    dirname = '/home/ubuntu/dataset/'
    name = 'compare.png'
    dirname += name
    proc = subprocess.Popen(['/home/ubuntu/OpenFace/openface/demos/classifier.py', 
        'infer', '/home/ubuntu/dataset/embedding/classifier.pkl', 
        dirname], 
        stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE
        )

    out, err = proc.communicate()

    name, confidence = out.split()
    print(name, confidence, dirname)

    return name, confidence, dirname
    

if __name__ == "__main__":
    while True:
        check = input("Insert input Data(I) or Training(T) or Compare(C) or QUIT(Q) : ")
        if check == 'I':
            detect.faceDetect()
        elif check == 'T':
            Train()
        elif check == 'Q':
            break
        elif check == 'C':
            Compare()
        else:
            print("INPUT ERROR")
