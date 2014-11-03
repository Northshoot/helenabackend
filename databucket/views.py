from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, Http404
from databucket.models import Firestorm, ObservedDevice , FirestormReading
from chartit import PivotDataPool, PivotChart, DataPool, Chart
from django.db.models import Count, Sum, Avg
import time

def home(request):
    n_dps = FirestormReading.objects.filter(acc_Z__lt =16000).filter( acc_Z__gt=-16000).order_by('recorded')
    if len(n_dps) > 900:
        n_dps = n_dps[:900]
    data_points="["
    for n in n_dps:
        data = "[%d,%d,%d]," %(n.acc_X, n.acc_Y,n.acc_Z)
        data_points+= data
    data_points+="[0,0,0]]"   
    
     
    return render_to_response('content.html',dict(data=data_points),
                              context_instance=RequestContext(request))
    
test_data ="[[1, 6, 5], [8, 7, 9], [1, 3, 4], [4, 6, 8], [5, 7, 7], [6, 9, 6], [7, 0, 5], [2, 3, 3], [3, 9, 8], [3, 6, 5], [4, 9, 4], [2, 3, 3], [6, 9, 9], [0, 7, 0], [7, 7, 9], [7, 2, 9], [0, 6, 2], [4, 6, 7], [3, 7, 7], [0, 1, 7], [2, 8, 6], [2, 3, 7], [6, 4, 8], [3, 5, 9], [7, 9, 5], [3, 1, 7], [4, 4, 2], [3, 6, 2], [3, 1, 6], [6, 8, 5], [6, 6, 7], [4, 1, 1], [7, 2, 7], [7, 7, 0], [8, 8, 9], [9, 4, 1], [8, 3, 4], [9, 8, 9], [3, 5, 3], [0, 2, 4], [6, 0, 2], [2, 1, 3], [5, 8, 9], [2, 1, 1], [9, 7, 6], [3, 0, 2], [9, 9, 0], [3, 4, 8], [2, 6, 1], [8, 9, 2], [7, 6, 5], [6, 3, 1], [9, 3, 1], [8, 9, 3], [9, 1, 0], [3, 8, 7], [8, 0, 0], [4, 9, 7], [8, 6, 2], [4, 3, 0], [2, 3, 5], [9, 1, 4], [1, 1, 4], [6, 0, 2], [6, 1, 6], [3, 8, 8], [8, 8, 7], [5, 5, 0], [3, 9, 6], [5, 4, 3], [6, 8, 3], [0, 1, 5], [6, 7, 3], [8, 3, 2], [3, 8, 3], [2, 1, 6], [4, 6, 7], [8, 9, 9], [5, 4, 2], [6, 1, 3], [6, 9, 5], [4, 8, 2], [9, 7, 4], [5, 4, 2], [9, 6, 1], [2, 7, 3], [4, 5, 4], [6, 8, 1], [3, 4, 0], [2, 2, 6], [5, 1, 2], [9, 9, 7], [6, 9, 9], [8, 4, 3], [4, 1, 7], [6, 2, 5], [0, 4, 9], [3, 5, 9], [6, 9, 1], [1, 9, 2]]"

def heat(request):
    n_dps = FirestormReading.objects.filter(acc_Z__lt =1200).filter( acc_Z__gt=-800).order_by('recorded')
    if len(n_dps) > 900:
        n_dps = n_dps[:900]
    data_points="["
 
    for n in n_dps:
        data = "[%d,%d,%d]," %(n.mag_X, n.mag_Y,n.mag_Z)
        data_points+= data
    data_points+="[0,0,0]]"    
    return render_to_response('heat_map.htm',dict(data=data_points),
                              context_instance=RequestContext(request))
def latest(request, amount):
    observationList = []
    total = ObservedDevice.objects.count()
    obsr = ObservedDevice.objects.all().order_by('seen')
    amount=int(amount)
    if amount >0 and total > amount:
        observationList = obsr[:amount]
    else:
        observationList = obsr
    return render_to_response('observation_list.html',{'observationList':observationList, 'total':total,'amount':amount},
                                  RequestContext(request)) 
def observations(request, fire_id):
    fire = None
    try:
        fire = Firestorm.objects.get(pk=fire_id)
        observationlist = ObservedDevice.objects.filter(observer=fire).order_by('seen')
        return render_to_response('observations.html',{'fire_id':fire_id, 'observationlist':observationlist},
                                  RequestContext(request)) 
    except Exception:
        return Http404("No such firestorm with id: %s", fire_id)
        
def firestorm(request,  amount):
    fireList = []
    if amount == 'all':
        fireList = Firestorm.objects.all().order_by('-seen')
        return render_to_response('firestorms.html',{'firestorms':fireList},
                                  RequestContext(request)) 
    else:
        fire = None
        try:
            fire = Firestorm.objects.get(pk=amount)
        except Exception:
            return Http404()
        
        #create analytics by device
        n_dps = FirestormReading.objects.filter(firestorm=fire).count()
        display_points= 20
        if display_points>n_dps:
            display_points = n_dps
        n_observ = ObservedDevice.objects.filter(observer=fire).count()  
        #observation= ObservedDevice.objects.filter(observer=fire)
        
        charts_firestorm=[]
        data = FirestormReading.objects.order_by('recorded').filter(firestorm=fire)[:display_points]
        #print data
        charts_firestorm.append(lightCharts(fire, display_points,data))
        charts_firestorm.append(accelerometerCharts(fire, display_points,data))
        charts_firestorm.append(magnetometerCharts(fire, display_points,data))
       
        #charts_firestorm.append(manucaftureCharts(fire, display_points, observation))
        return render_to_response('single_info.html',{'fire_id':fire.pk,
                                                      'n_dps':n_dps, 
                                                      'display_points':display_points,
                                                      'n_observ':n_observ,
                                                      'charts':charts_firestorm},
                                  RequestContext(request)) 

def manucaftureCharts(fire, number, data):
    ds = DataPool(
       series=
        [{'options': {
            'source': data},
          'terms': [
            'manufactorer',
            'observer']}
         ])

    #print data

    manucaftureCharts = Chart(
            datasource = ds, 
            series_options = 
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                  'manufactorer': [
                    'observer']
                  }}],
            chart_options = 
              {'title': {
                   'text': 'Monthly Temperature of Boston'}})
    
    return manucaftureCharts

def accelerometerCharts(fire, number, data):

    ds = DataPool(
       series=
        [{'options': {
            'source': data},
          'terms': [
            ('recorded', lambda d: d.strftime("%H:%M:%S")),
            'acc_X',
            'acc_Y',
            'acc_Z']}])

    accelerometerCharts = Chart(
            datasource = ds, 
            series_options = 
              [{'options':{
                  'type': 'line',
                  'xAxis': 0,
                  'yAxis': 0,
                  'zIndex': 1},
                'terms':{
                  'recorded': [
                    'acc_X',
                    'acc_Y',
                    'acc_Z']}}],
            chart_options = 
              {'title': {
                   'text': 'Accelerometer data'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
    return accelerometerCharts

def lightCharts(fire, number, data):

    ds = DataPool(
       series=
        [{'options': {
            'source': data},
          'terms': [
            'firestorm__local_mac',
            'light']}])

    lightCharts = Chart(
            datasource = ds, 
            series_options = 
              [
               {'options': {
                  'type': 'scatter'},
                'terms':{
                  'firestorm__local_mac': ['light']}}],
            chart_options = 
              {'title': {
                   'text': 'LUX'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
    return lightCharts

def magnetometerCharts(fire, number, data):

    ds = DataPool(
       series=
        [{'options': {
            'source': data},
          'terms': [
            ('recorded', lambda d: d.strftime("%H:%M:%S")),
            'mag_X',
            'mag_Y',
            'mag_Z']}])

    magnetometerCharts = Chart(
            datasource = ds, 
            series_options = 
              [{'options':{
                  'type': 'line',
                  'xAxis': 0,
                  'yAxis': 0,
                  'zIndex': 1},
                'terms':{
                  'recorded': [
                    'mag_X',
                    'mag_Y',
                    'mag_Z']}}],

            chart_options = 
              {'title': {
                   'text': 'Magnetometer data'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})
    return magnetometerCharts

def analytics(request):
    data = Firestorm.objects.all().order_by('seen')
    firestormpivotdata = DataPool(
       series=
        [{'options': {
            'source': data},
          'terms': [
            'local_mac',
            'observations', 
            'data_points']}
         ])
    
    #Step 2: Create the PivotChart object
    firestormdata = Chart(
        datasource = firestormpivotdata, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms':{
              'local_mac': [
                'observations',
                'data_points']
              }}],
        chart_options = 
          {'title': {
               'text': 'Number of Observations and Data points per Firestorm'},
           'xAxis': {
                'title': {
                   'text': 'MAC of Firestrom'}}})

    light_points = FirestormReading.objects.all().order_by('recorded')
    ds = DataPool(
       series=
        [{'options': {
            'source': FirestormReading.objects.all()},
          'terms': [
            'firestorm',
            'light']}
         ])

    lightdata = Chart(
        datasource = ds, 
        series_options = 
          [{'options':{
              'type': 'dot',
              'stacking': False},
            'terms':{
              'firestorm': [
                'light']
              }}])
    
    return render_to_response('analytics.html',{'charts':[firestormdata, lightdata]},
                                  RequestContext(request)) 
    

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
    l_MAC = fire_data.pop('observer')[0]
    #check if firestorm exist
    fire, v = Firestorm.objects.get_or_create(local_mac=l_MAC)
    fire_data['observer']= fire
    obsr = ObservedDevice.objects.create(observer = fire_data['observer'],
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
    #print sensor_data
    fire = sensor_data.pop('firestorm')[0]
    #print fire
    sensor_data = dict((k,int(v)) for k,v in sensor_data.iteritems())

    #check if firestorm exist
    fire, v = Firestorm.objects.get_or_create(pk=fire)
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

