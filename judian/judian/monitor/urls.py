from django.conf.urls import url
from django.conf.urls import include

#from monitor.views import HostCreateView, HostDetailView
from rest_framework import routers
from .views import HostViewSet
router = routers.DefaultRouter()
router.register(r'host', HostViewSet)

urlpatterns = [
    # monitor/v1/host/
    #url(r'^host/$', HostCreateView.as_view(), name='host.get'),
    # monitor/v1/host/<pk>
    #url(r'^host/(?P<id>[0-9]+)$', HostDetailView.as_view(), name='host.detail'),
    url(r'^', include(router.urls)),
]
