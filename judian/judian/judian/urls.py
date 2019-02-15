"""
Definition of urls for judian.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

import app.forms
import app.views

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # REST API
    # support DRF's login/logout views
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # with above you can use /api-auth/login & /api-auth/logout
    # after you type /api-auth/login and login ok, it will show an error complain
    # about /accounts/profile/, don't worry for that
    url(r'^monitor/v1/', include('monitor.urls')), # monitor.urls.py 是下一層的 url 要自己寫
]
