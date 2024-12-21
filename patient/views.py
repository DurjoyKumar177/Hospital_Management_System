from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode #urls create kore encode and decode korar janno
from django.utils.encoding import force_bytes #akti function ja encoding ke aro efficient kore dei
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

#for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
class PatientsViewset(viewsets.ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer
    
class UserRegistrationApiview(APIView):
    serializer_class = serializers.RegistrationSerializer 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid= urlsafe_base64_encode(force_bytes(user.pk))# user er akti unique id create kore dei
            conferm_link = f"http://localhost:8000/patient/verify/{uid}/{token}"
            email_subject = "Please activate your account"
            email_body = render_to_string('confirm_email.html',{'confirm_link' : conferm_link})
            
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            return Response("Check your email for confirmation" , status=201)
        return Response(serializer.errors)

def verify(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponseBadRequest("Activation link is invalid")
    
class UserLoginApiview(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password) #user authenticate function to verify username and password is currect or not
            
            if user :
                token,_ = Token.objects.get_or_create(user=user) #get_or_create function token thakle nibe ar na thakle create kore dibe. akhane create token er janno _ user kora hoice.
                return Response({'token':token.key, 'user_id':user.id})
            else:
                return Response({'error': 'Invalid credentials'})
        return Response(serializer.errors)