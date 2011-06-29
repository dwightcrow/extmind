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

def queue( request ):
    c = {}
    return render_to_response( 'queue.html', c,
                               context_instance=RequestContext(request) )

    return HttpResponse( "this is going to be q page" );

def concepts( request ):
    return HttpResponse( "this is going to be ceoncepts page" );

def session( request ):
    return HttpResponse( "this is going to be session page" );

def calendar( request ):
    return HttpResponse( "this is going to be calendar page" );
