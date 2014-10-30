from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse
from databucket.models import Firestorm, ObservedDevice , FirestormReading

def home(request):
    return render_to_response('content.html',dict(test="heelloooo"),
                              context_instance=RequestContext(request))
    
def firestorm(request,  amount):
    fireList = []
    fire_id=None
    try:
        fire_id = int(amount)
    except ValueError:
        pass
    
    if fire_id:
        try:
            fireList += Firestorm.objects.get(pk=fire_id)
        except Exception:
            pass

    elif amount == 'all':
        fireList = Firestorm.objects.all()
    return render_to_response('firestorms.html',dict(firestorms=fireList),
                              RequestContext(request)) 
##must be ints!
sensor_readings={'acc_X':120,'acc_Y':120,'acc_Z':120,'mag_X':120,'mag_Y':120,'mag_Z':120} 
test_data = {'observer': '0xffffffff', 'observation': '0xeeeeeeeee', 
                              'sensor_data':sensor_readings
                              }
s_data = {'observer': '0xffffffff', 'observation': '0xeeeeeeeee'}


from django.views.decorators.csrf import csrf_exempt                                          
@csrf_exempt    
def firestormAdd(request, action):

    if action == 'observation':
        return addObservation(request)
    elif action == 'sensordata':
        return addSensorReading(request)
    else:
        return HttpResponse("Unsupported command")
@csrf_exempt  
def addObservation(request):
    '''
    removed try to easy debug in case of error
    '''
    fire_data = request.POST.copy()
    #check if firestorm exist
    fire, v = Firestorm.objects.get_or_create(local_mac=fire_data.pop('observer'))
    fire.save()
    fire_data['observer']= fire
    obsr = ObservedDevice.objects.create(observer = fire,
                                             observedMAC=fire_data['observedMAC'],
                                            manufactorer=fire_data['manufactorer']  )
    obsr.save()
    return HttpResponse("OK")

    
@csrf_exempt  
def addSensorReading(request):
    '''
    removed try to easy debug in case of error
    '''
    sensor_data = request.POST.copy()
    fire = sensor_data.pop('firestorm')
    sensor_data = dict((k,int(v)) for k,v in sensor_data.iteritems())

    #check if firestorm exist
    fire, v = Firestorm.objects.get_or_create(pk=fire)
    fire.save()
    reading = FirestormReading.objects.create(firestorm=fire,
                                              acc_X=sensor_data['acc_X'],
                                              acc_Y=sensor_data['acc_Y'],
                                              acc_Z=sensor_data['acc_Z'],
                                              mag_X=sensor_data['mag_X'],
                                              mag_Y=sensor_data['mag_Y'],
                                              mag_Z=sensor_data['mag_Z'],
                                              light=sensor_data['light'])
    reading.save()
    return HttpResponse("OK")

