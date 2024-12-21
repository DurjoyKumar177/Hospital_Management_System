from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ContactsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContuctUsSerializer