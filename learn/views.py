from django.contrib.auth import authenticate, login as django_login, \
    logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.models import User
from extmind.learn.models import Concept, Goal 
from extmind.learn.forms import RegistrationForm, LoginForm

import datetime

daysOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                         "Saturday", "Sunday" )

def queue( request ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    c = {}
    c['showConcept'] = False
    if 'concept' in request.GET and request.GET['concept'] != '':
        newConcept = Concept()
        newConcept.name = request.GET['concept']
        newConcept.user = User.objects.get(id=1)
        newConcept.save()
        c['submittedConcept'] = request.GET['concept']
        c['showConcept'] = True
    return render_to_response( 'queue.html', c,
                               context_instance=RequestContext(request) )

def concepts( request ):
    c = {}
    c['concepts'] = Concept.objects.filter( user=request.user ).exclude(text='').order_by('-date').all()
    return render_to_response( 'concepts.html', c,
                               context_instance=RequestContext(request) )

def session( request ):
    c = {}
    weekday = daysOfWeek[ datetime.date.today().weekday() ].upper()
    numGoalPerDay = Goal.objects.filter( user=request.user).filter( day=weekday ).count()
    if numGoalPerDay == 0:
        goal = Goal()
        goal.day = weekday
        goal.user = request.user
        goal.length = int(0)
        goal.save()
    elif numGoalPerDay == 1:
        goal = Goal.objects.filter( user=request.user).filter( day=weekday ).all()[0]
    else:
        assert 0, 'weird num goals %d' % numGoalPerDay
    c['goal'] = goal
    c['concepts'] = Concept.objects.filter( user=request.user ).filter(text="").order_by('-date').all()
    if Concept.objects.filter( user=request.user ).filter(text="").order_by('-date').count() == 0:
        c['noConcepts'] = True
    else:
        c['noConcepts'] = False
    c['first'] = c['concepts'][0]
    return render_to_response( 'session.html', c,
                               context_instance=RequestContext(request) )
@csrf_exempt
def saveText( request, conceptId ):
    concept = Concept.objects.get( id=conceptId )
    concept.text = request.POST['text']
    concept.date = datetime.datetime.now()
    concept.save()
    return HttpResponse( "Success");

class wrapper():
    def __init__(self, day, minutes):
        self.day = day
        self.minutes = minutes

def settings( request ):
    c={}
    prevSettings = []
    for d in daysOfWeek:
        numGoalPerDay = Goal.objects.filter( user=request.user).filter( day=d.upper() ).count()
        if numGoalPerDay == 0:
            prevSettings.append( wrapper(d,0) )
        elif numGoalPerDay == 1:
            goal = Goal.objects.filter( user=request.user).filter( day=d.upper() ).all()[0]
            prevSettings.append( wrapper(d, goal.length) )
        else:
            assert 0, "wrong number of goals: %d" % numGoalPerDay
    assert len( prevSettings ) == 7
    c['prevSettings'] = prevSettings
    return render_to_response( 'settings.html', c,
                               context_instance=RequestContext(request) )

@csrf_exempt
def saveSettings( request ):
    for d in daysOfWeek:
        assert d.upper() in request.POST
        length = request.POST[d.upper()]
        numGoalPerDay = Goal.objects.filter( user=request.user).filter( day=d.upper() ).count()
        if numGoalPerDay == 0:
            goal = Goal()
            goal.day = d.upper()
            goal.user = request.user
            goal.length = int(length)
        elif numGoalPerDay == 1:
            goal = Goal.objects.filter( user=request.user).filter( day=d.upper() ).all()[0]
            goal.length = int(length)
        else:
            assert 0, "wrong number of goals: %d" % numGoalPerDay
        goal.save()
    return HttpResponse( "Success ")

def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password1'])
            # I should add null goals here - get rid of ifs...
            django_login(request, user)
            return HttpResponseRedirect(reverse(queue)) # Redirect after POST
    else:
        form = RegistrationForm() # An unbound form
    return render_to_response("registration/register.html", {'form': form}, 
                              context_instance=RequestContext(request))
    
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse(queue))
