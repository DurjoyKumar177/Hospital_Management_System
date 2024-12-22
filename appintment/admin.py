from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Register your models here.
class AppintmentAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'patient_name', 'appintment_status', 'appintment_type', 'symptoms', 'time', 'cancel')

    def doctor_name(self, obj):
        return obj.doctor.user.first_name 

    def patient_name(self, obj):
        return obj.patient.user.first_name
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.appintment_status =='Running' and obj.appintment_type == 'Online':
            email_subject = "Your appintment is running"
            email_body = render_to_string('admin_email.html',{'user' : obj.patient.user, 'doctor' : obj.doctor})
            
            email = EmailMultiAlternatives(email_subject,'',to=[obj.patient.user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
        return super().save_model(request, obj, form, change)
    
admin.site.register(models.Appintment, AppintmentAdmin)