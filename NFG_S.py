#!/usr/bin/env python3
import subprocess
import sys

pre_name = 'NoNo'

def Train():
    proc = subprocess.Popen(['/root/openface/util/align-dlib.py', '/root/openface/training-images/', 
        'align', 'outerEyesAndNose',
        '/root/openface/aligned-images/', 
        '--size', '96'],
        stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
    out, err = proc.communicate()
    print('==========ALIGN THE IMAGE COMPLETE==========')
    proc = subprocess.Popen(['/root/openface/batch-represent/main.lua', 
        '-outDir', '/root/openface/generated-embeddings/', 
        '-data', '/root/openface/aligned-images/'], 
        stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )

    out, err = proc.communicate()
    print('==========EMBEDDING IMAGE COMPLETE==========')
    proc = subprocess.Popen(['rm', '/root/openface/aligned-images/cache.t7'])

    out, err = proc.communicate()
    proc = subprocess.Popen(['/root/openface/demos/classifier2.py', 'train', '/root/openface/generated-embeddings/'],
                stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    
    out, err = proc.communicate()
    print ("==========TRAIN IMAGES COMPLETE==========")


def Compare(a):
    global pre_name
   # print (a)
    dirname = '/root/openface/compare/'
  #  name = ''
    dirname += a
   # print ('dirname = ',dirname)
    proc = subprocess.Popen(['/root/openface/demos/classifier2.py', 
        'infer', '/root/openface/generated-embeddings/classifier.pkl', 
        dirname], 
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
    

if __name__ == "__main__":
    sss = ''
    while True:
        check = input("Insert input Data(I) or Training(T) or Compare(C) or QUIT(Q) : ")
#       if check == 'I':
#          detect.faceDetect()
        if check == 'T':
            Train()
        elif check == 'Q':
            break
        elif check == 'C':
            for i in range(1, 24):
                sss = 'compare_' + str(i) + '.jpg'
                Compare(sss)
        else:
            print("INPUT ERROR")

