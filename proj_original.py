from gpiozero import MotionSensor, Button, LED
import time
from time import sleep    
from picamera import PiCamera
import os
import requests
import boto3
from botocore.client import Config
import json

def flash(value):
    if value:
        flash1.on()
        flash2.on()
        flash3.on()
        flash4.on()
        flash5.on()
    else:
        flash1.off()
        flash2.off()
        flash3.off()
        flash4.off()
        flash5.off()
    
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print ("---  new folder...  ---")
        print ("---  OK  ---")
    else:
        print ("---  There is this folder!  ---")

#ACCESS_KEY_ID = 'AKIAIY3RGAGIQKSH4KBA'
#ACCESS_SECRET_KEY = '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'
        
ACCESS_KEY_ID = 'AKIAJH5WE2AXDHHZ6OGA'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'csee4764'#this does not to be changed

payload = {"username":"user1","emailNum":0}
headers = {"Content-Type": "application/json"}
# button17 = Button(17)
pir = MotionSensor(17)
mailLock = MotionSensor(27)
camera = PiCamera()
camera.rotation = 90
numMail = 0
signal = LED(2)
flash1 = LED(9)
flash2 = LED(10)
flash3 = LED(11)
flash4 = LED(20)
flash5 = LED(21)
signal.off()
flash(0)
sleep(0.5)
signal.on()
sleep(0.5)
signal.off()
sleep(0.5)
signal.on()

# mailLock.when_motion = FUNCTION
url_loc = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBbGEjWKnZGQmE12n6ieVIGi0IUxqUFYs4'
d = {
  "homeMobileCountryCode": 310,
  "homeMobileNetworkCode": 410,
  "radioType": "gsm",
  "carrier": "Vodafone",
  "considerIp": "true",
  "cellTowers": [
          {"cellTowers": [{"cellId": 42,
                                  "locationAreaCode": 415,
                                  "mobileCountryCode": 310,
                                  "mobileNetworkCode": 410,
                                  "age": 0,
                                  "signalStrength": -60,
                                  "timingAdvance": 15
                           }]
           }
  ],
  "wifiAccessPoints": [
      {
              "macAddress": "00:25:9c:cf:1c:ac",
              "signalStrength": -43,
              "age": 0,
              "channel": 11,
              "signalToNoiseRatio": 0
              }
  ]
}

r_loc = requests.post(url_loc, data = json.dumps(d))
print(r_loc.json())
lat = r_loc.json()['location']['lat']
lng = r_loc.json()['location']['lng']

#lat = 40.808
#lng = -73.9655

upLoadBoardLoc = {"locationtwo": "boardLatitude"+str(lat)+"boardLongitude"+str(lng),"board": "board1"}
r = requests.post("https://3drfiyermc.execute-api.us-east-1.amazonaws.com/dev/location", data=json.dumps(upLoadBoardLoc),headers=headers)
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print(r.json())

while True:
    if mailLock.motion_detected:
        print ("hello")
        
        numMail = 0
        payload = {"username":"user1","emailNum":0}
        payload["emailNum"] = numMail
        r = requests.post("https://3drfiyermc.execute-api.us-east-1.amazonaws.com/dev/cs4764/insertdatabase", data=json.dumps(payload),headers=headers)
        payload = {"userid":"user1"}
        r = requests.post("https://3drfiyermc.execute-api.us-east-1.amazonaws.com/dev/openboxdelete", data=json.dumps(payload),headers=headers)
        print(r.json())
    
    # pir.wait_for_motion()
    # pir.wait_for_no_motion(timeout = 2.5)
    if not pir.motion_detected:
        print("Motion detected!")  
        signal.off()
        camera.start_preview()
        flash(1)
        sleep(2.5)
        
        ticks = time.localtime(time.time())
        for t in ticks:
            print(t, type(t))
        t = ticks
                
        
        
        path = "/home/pi/Desktop/photo/%d_%d_%d" % (t[0], t[1], t[2])
        filename = "user1_%d_%d_%d_%d_%d_%d.jpg" % (t[0], t[1], t[2], t[3], t[4], t[5])
        path_name = path+'/'+filename
        mkdir(path)
        camera.capture(path_name)
        numMail = numMail+1
        camera.stop_preview()
        flash(0)
        
        
        FILE_NAME = filename  # this can be cahanged to your picture name
        data = open(path_name, 'rb')
        # S3 Connect
        s3 = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        #Up9t3o0PCP+q8e+T3eI1InevJIfm/w2GGjVP6VdM
        #Up9t3o0PCP+q8e+T3eI1InevJIfm/w2GGjVP6VdM
        # Image Uploaded
        s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ACL='public-read')
        print ("Upload to server Done")
        
        #r = requests.get("https://3drfiyermc.execute-api.us-east-1.amazonaws.com/dev/cs4764/sendemail")
        payload = {"username":"user1","emailNum":0}
        payload["emailNum"] = numMail
        r = requests.post("https://3drfiyermc.execute-api.us-east-1.amazonaws.com/dev/cs4764/insertdatabase", data=json.dumps(payload),headers=headers)
        
        sleep(2)
        signal.on()
        print ("All Done")
    else:
        print("Nothing happend...")

    print(numMail)
    sleep(0.5)
        

