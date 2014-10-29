'''
Created on Oct 28, 2014

@author: lauril
'''

import requests
#example data, see model for what can be added
def addObservation(payload = {'observer': '0xffffffff', 'observation': '0xeeeeeeeee', 
                              'sensor_data':
                                          {'acc_X':'120',
                                            'acc_Y':'120',
                                            'acc_Z':'120',
                                            'mag_X':'120',
                                            'mag_Y':'120',
                                            'mag_Z':'120'}
                              }
                   ):
                   
    
    base_url = "http://127.0.0.1:8000/firestorm/add/"
    r = requests.post(base_url, data=payload)
    print(r.text)
    

if __name__ == "__main__":
    addObservation()