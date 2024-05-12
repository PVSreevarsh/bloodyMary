from django.db import models
from datetime import datetime,timedelta
import uuid

import json
import uuid
from django.db import models
from django.db.models import Max

class Bank(models.Model):
    name = models.CharField(max_length=255)  # Name of the bank
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)

class Sector(models.Model):
    name = models.CharField(max_length=255)  # Name of the sector
    risk_classification = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    total_ask = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)

class Investment(models.Model):
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE)
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    timestamp= models.DateTimeField(auto_now_add=True) 


class SME(models.Model):
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE)
    askamt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)
    givenamt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)
    name = models.CharField(max_length=255) 
    label = models.CharField(max_length=255,  null=True, blank=True)
    gstn = models.CharField(max_length=255)
    amtpaid= models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)
    phoneNumber=models.CharField(max_length=255, null=True, blank=True)
    


