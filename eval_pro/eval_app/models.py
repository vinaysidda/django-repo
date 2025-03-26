from django.db import models

# Create your models here.
class GPT(models.Model):
    model_name =models.CharField(max_length=100)
    model_access = models.FloatField(default=0.0)
    model_latency = models.FloatField(default=0.5)

class RTT(models.Model):
    model_name =models.CharField(max_length=100)
    model_access = models.FloatField(default=0.0)
    model_latency = models.FloatField(default=0.5)
    
class Business(models.Model):
    name=models.CharField(max_length=255)
    revenue=models.FloatField(default=0.0)
    profit=models.FloatField(default=0.0)
    employees=models.IntegerField()
    country=models.CharField(max_length=255)
 
    def __str__(self):
        return self.name
