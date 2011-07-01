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
from extmind.learn.models import Concept 
from extmind.learn.forms import RegistrationForm, LoginForm

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
    c['concepts'] = Concept.objects.filter( user=request.user ).filter(text="").order_by('-date').all()
    return render_to_response( 'session.html', c,
                               context_instance=RequestContext(request) )
@csrf_exempt
def saveText( request, conceptId ):
    concept = Concept.objects.get( id=conceptId )
    concept.text = request.POST['text']
    concept.save()
    return HttpResponse( "Success");

def settings( request ):
    c={}
    return render_to_response( 'settings.html', c,
                               context_instance=RequestContext(request) )


def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password1'])
            django_login(request, user)
            return HttpResponseRedirect(reverse(queue)) # Redirect after POST
    else:
        form = RegistrationForm() # An unbound form
    return render_to_response("registration/register.html", {'form': form}, 
                              context_instance=RequestContext(request))
    
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse(queue))
