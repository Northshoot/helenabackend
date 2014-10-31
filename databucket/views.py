from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, Http404
from databucket.models import Firestorm, ObservedDevice , FirestormReading
from chartit import PivotDataPool, PivotChart, DataPool, Chart
from django.db.models import Count, Sum, Avg
import time

def home(request):
    return render_to_response('content.html',dict(test="heelloooo"),
                              context_instance=RequestContext(request))

def observations(request, fire_id):
    fire = None
    try:
        fire = Firestorm.objects.get(pk=fire_id)
        observationlist = ObservedDevice.objects.filter(observer=fire)
        return render_to_response('observations.html',{'fire_id':fire_id, 'observationlist':observationlist},
                                  RequestContext(request)) 
    except Exception:
        return Http404("No such firestorm with id: %s", fire_id)
        
def firestorm(request,  amount):
    fireList = []
    if amount == 'all':
        fireList = Firestorm.objects.all()
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
        data = FirestormReading.objects.filter(firestorm=fire)[:display_points]
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

    print data

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

def lightCharts(fire, number,data):

    ds = DataPool(
       series=
        [{'options': {
            'source': data},
          'terms': [
            ('recorded', lambda d: d.strftime("%H:%M:%S")),
            'light']}])

    lightCharts = Chart(
            datasource = ds, 
            series_options = 
              [
               {'options': {
                  'type': 'area'},
                'terms':{
                  'recorded': ['light']}}],
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
    firestormpivotdata = DataPool(
       series=
        [{'options': {
            'source': Firestorm.objects.all()},
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
    
    #manufacturers
#     ds = DataPool(
#        series=
#         [{'options': {
#             'source': FirestormReading.objects.order_by('-recorded')[:20]},
#           'terms': [
#             ('recorded', lambda d: d.strftime("%H:%M:%S")),
#             'firestorm',
#             'light']}
#          ])
# 
#     lightdata = Chart(
#         datasource = ds, 
#         series_options = 
#           [{'options':{
#               'type': 'line',
#               'stacking': False},
#             'terms':{
#               'firestorm': [
#                 'recorded',
#                 'light']
#               }}],
#         chart_options = 
#           {'title': {
#                'text': 'Weather Data of Boston and Houston'},
#            'xAxis': {
#                 'title': {
#                    'text': 'Firestorm'}}})

    ds = DataPool(
          series= [{'options': {
            'source': FirestormReading.objects.all()[:100]},
          'terms': [
            'firestorm__local_mac', 
            'light']}])
    
    lightdata = Chart(
              datasource = ds, 
              series_options = 
          [{'options':{
              'type': 'scatter'},
            'terms':{
              'firestorm__local_mac': [
                'light']
              }}],
             chart_options =
              {'title': {
                   'text': 'Average sensed light by Firestorm'},
               'xAxis': {
                    'title': {
                       'text': 'Firestorm'}},
               'yAxis': {
                    'title': {
                       'text': 'Lux'}}}
                           )
    
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
    print sensor_data
    fire = sensor_data.pop('firestorm')[0]
    print fire
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

