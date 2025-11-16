from django.db import models

class GetMoney(models.Model):
    userID = models.CharField(max_length=30)
    budgetTot = models.CharField(max_length=30)
    transTot = models.CharField(max_length=30)
# Create your models here.
