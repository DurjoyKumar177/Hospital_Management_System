from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class AppintmentsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Appintment.objects.all() #ei queryset built in sobar janno
    serializer_class = serializers.AppintmentSerializer
    
    # Custom Query er janno
    def get_queryset(self):
        queryset = super().get_queryset() #8 no liner er parent ke inherit korlam ekhane
        patient_id = self.request.query_params.get('patient_id') #here query_params is query parameter
        if patient_id :
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
    
    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id :
            queryset = queryset.filter(doctor_id=doctor_id)
        return queryset