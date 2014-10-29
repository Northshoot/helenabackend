from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse
from databucket.models import Firestorm, ObservedDevice 

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

from django.views.decorators.csrf import csrf_exempt                                          
@csrf_exempt    
def firestormAdd(request):
    post = request.POST.copy()
    fire = None
    try:
        #check if firestorm exist
        fire = Firestorm.objects.get_or_create(pk=post.get('observer'))
        
    except Exception as e:
        return HttpResponse("Error with fire  object: %s" %e)
    
    return HttpResponse("OK")