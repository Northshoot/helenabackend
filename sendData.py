'''
Created on Oct 28, 2014

@author: lauril
'''

import requests
#example data, see model for what can be added

sensor_readings={'firestorm': '0xfffffff4', 'acc_X':'120','acc_Y':'130','acc_Z':'140','mag_X':'50','mag_Y':'60','mag_Z':'60','light':'9000'} 
observation = {'observer': '0xfffffff5', 'observedMAC': '0xeeeeeeeee' , 'manufactorer':'234'}
base_url = "http://127.0.0.1:8000/firestorm/add/"


def addObservation(payload  ):
    r = requests.post(base_url+"observation/", data=payload)
    text_file = open("out.html", "w")
    print r.text
    text_file.write(r.text)
    
def addFirestormReading(payload):
    r = requests.post(base_url+"sensordata/", data=payload)
    text_file = open("out-observation.html", "w")
    text_file.write(r.text)
    print r.text
    
if __name__ == "__main__":
    #addObservation(observation)
    addFirestormReading(sensor_readings)