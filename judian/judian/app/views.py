"""
Definition of views.
"""
import random
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
#from django.template import RequestContext

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    context = {}
    context['title'] = 'Home Page'
    context['year'] = datetime.now().year
    #return render(
    #    request,
    #    'app/index.html',
    #    {
    #        'title':'Home Page',
    #        'year':datetime.now().year,
    #    }
    #)
    return render(request, 'app/index.html', context
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    #return render(
    #    request,
    #    'app/about.html',
    #    {
    #        'title':'About',
    #        'message':'Your application description page.',
    #        'year':datetime.now().year,
    #    }
    #)
    context = {}
    context['title'] = 'About'
    context['message'] = 'Your application description page.'
    context['year'] = datetime.now().year
    # add some dummy data
    names = ("bob", "dan", "jack", "lizzy", "susan")
    items = []
    for i in range(10):
        items.append({
            "name": random.choice(names),
            "age": random.randint(20,80),
            "url": "https://example.com",
        })
    context["items"] = items
    return render(request, 'app/about.html', context)
