from django.db import models

# Create your models here.
class DailyCalendar(models.Model):
    name = models.CharField(max_length=100, unique=True)
    numIndex = models.IntegerField(default=-1)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class MonthlyCalendar(models.Model):
    name = models.CharField(max_length=100)
    houseNum = models.IntegerField(default=-1)
    houseSymbol = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
