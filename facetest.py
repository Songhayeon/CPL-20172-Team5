########### Python 3.6 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json
import cv2
import random
import urllib.request
import ftplib
import numpy as np
###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '09413c4eb71b4a6ab71c85b76d3beffc'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'https://westcentralus.api.cognitive.microsoft.com/'

# Request headers.
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters.
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,glasses',
}

# Body. The URL of a JPEG image to analyze.
#imageURL = 'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'
imageURL = 'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'
body = {'url': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'}

imageName = "target.jpg"
urllib.request.urlretrieve(imageURL, imageName)
image = cv2.imread(imageName, cv2.IMREAD_COLOR)
print("Got image")
## height, width, channels = image.shape

try:
    # Execute the REST API call and get the response.
    response = requests.request('POST', uri_base + '/face/v1.0/detect', json=body, data=None, headers=headers, params=params)

    print ('Response:')
    parsed = json.loads(response.text)
    faceRect = parsed[0]['faceRectangle']
    left = faceRect['left']
    top = faceRect['top']
    height = faceRect['height']
    width = faceRect['width']
    print("Got dot data")
    cv2.rectangle(image, (left, top), (left + width, top + height), (255, 0, 0), 3, 4, 0)
    cv2.imshow('Image', image)
    cv2.imwrite("./test.jpg", image)

    print (json.dumps(parsed, sort_keys=True, indent=2))

except Exception as e:
    print('Error:')
    print(e)


cv2.waitKey(0)
cv2.destroyAllWindows()
