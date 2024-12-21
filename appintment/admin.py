from django.contrib import admin
from . import models

# Register your models here.
class AppintmentAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'patient_name', 'appintment_status', 'appintment_type', 'symptoms', 'time', 'cancel')

    def doctor_name(self, obj):
        return obj.doctor.user.first_name 

    def patient_name(self, obj):
        return obj.patient.user.first_name
    
admin.site.register(models.Appintment, AppintmentAdmin)