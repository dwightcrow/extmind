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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    c = {}
    c['concepts'] = Concept.objects.filter( user=request.user ).exclude(text='').order_by('-date').all()
    return render_to_response( 'concepts.html', c,
                               context_instance=RequestContext(request) )

def session( request ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
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
    if len(c['concepts']) > 0:
        c['first'] = c['concepts'][0]
    return render_to_response( 'session.html', c,
                               context_instance=RequestContext(request) )
@csrf_exempt
def saveText( request, conceptId ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    u_profile = request.user.profile
    c={}
    prevSettings = [ wrapper('Monday', u_profile.monMin),
                     wrapper('Tuesday', u_profile.tueMin),
                     wrapper('Wednesday', u_profile.wedMin),
                     wrapper('Thursday', u_profile.thuMin),
                     wrapper('Friday', u_profile.friMin),
                     wrapper('Saturday', u_profile.satMin),
                     wrapper('Sunday', u_profile.sunMin), ]
    c['prevSettings'] = prevSettings
    c['emailRemind'] = u_profile.emailRemind
    c['textRemind'] = u_profile.textRemind
    c['phoneRemind'] = u_profile.phoneRemind
    c['phoneNumber'] = u_profile.phoneNumber
    return render_to_response( 'settings.html', c,
                               context_instance=RequestContext(request) )

@csrf_exempt
def saveSettings( request ):
    u = request.user
    print u
    u_profile = u.profile
    print u_profile
    # save minutes
    for d in daysOfWeek:
        assert d.upper() in request.POST
        minutes = request.POST[d.upper()]
        print minutes
        print dir( u_profile )
        print u_profile.monMin
        u_profile.monMin = int(minutes)
        print u_profile.monMin
        print d.lower()[:3] + 'Min' + '= ' + minutes
        u_profile.__setattr__( d.lower()[:3] + 'Min', int(minutes) )
        print u_profile
    # save reminders and phone number
    u_profile.emailRemind = ( request.POST['emailRemind'] == 'true' )
    u_profile.textRemind = ( request.POST['textRemind'] == 'true' )
    u_profile.phoneRemind = ( request.POST['phoneRemind'] == 'true' )
    u_profile.phoneNumber = ( request.POST['phoneNumber'] )
    u_profile.save()
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

def phoneRemind(request):
    c = {}
    return render_to_response("phoneRemind", c, 
                              context_instance=RequestContext(request))

