from django.db import models
from doctor.models import Doctor, AvailableTime
from patient.models import Patient
# Create your models here.

APPINTMENT_STATUS = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
    ('Running', 'Running'),
]

APPINTMENT_TYPE = [
    ('Online', 'Online'),
    ('Offline', 'Offline'),
]

class Appintment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appintment_status = models.CharField(max_length=10, choices=APPINTMENT_STATUS, default='Pending')
    appintment_type = models.CharField(max_length=10, choices=APPINTMENT_TYPE, default='Offline')
    symptoms = models.TextField()
    time = models.ForeignKey(AvailableTime, on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Patient: {self.patient.user.first_name} {self.patient.user.last_name} - Doctor: {self.doctor.user.first_name} {self.doctor.user.last_name}"
