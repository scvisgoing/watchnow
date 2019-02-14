from django.shortcuts import render

from rest_framework import viewsets  # then we use HostViewSet
from .serializers import HostSerializer
from .models import Host
class HostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    #permission_classes = (permissions.IsAuthenticated, IsOwner)
