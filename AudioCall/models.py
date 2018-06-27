from django.db import models

# Create your models here.


class CallDetail(models.Model):
    call_sid = models.CharField(max_length=64, unique=True)
    call_from = models.CharField(max_length=64)
    call_to = models.CharField(max_length=64)
    country_name = models.CharField(max_length=256, null=True, blank=True)
    comment = models.CharField(max_length=256, null=True, blank=True)
    went_conference = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


SUBJECT_CHOICES = (
        (1, 'RPbox'),
        (2, 'Data consultancy')
    )


class Contact(models.Model):
    name = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=64)
    subject = models.IntegerField(choices=SUBJECT_CHOICES)
    comment = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
