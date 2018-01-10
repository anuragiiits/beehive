from django.db import models
from UserAuth.models import CustomUser


class NewEvents(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    #user, fullname, phone number
    applied_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(NewEvents, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
