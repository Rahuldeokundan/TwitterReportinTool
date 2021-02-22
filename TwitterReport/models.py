from django.db import models

# Create your models here.

class DataSet(models.Model):
    currentDate=models.CharField(max_length=120)
    account = models.CharField(max_length=120)
    spend = models.CharField(max_length=120)
    StartDate = models.CharField(max_length=120)
    EndDate = models.CharField(max_length=120)

    def __str__(self):
        return self.account