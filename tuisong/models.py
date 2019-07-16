from django.db import models

# Create your models here.


class SiteConfig(models.Model):
    siteid = models.CharField(max_length=30, unique=True)
    source = models.CharField(max_length=256)


class Quotation(models.Model):
    siteid = models.ForeignKey(SiteConfig, on_delete=models.CASCADE)
    transaction_pair = models.CharField(max_length=100)
    buy1 = models.CharField(max_length=100)
    buy2 = models.CharField(max_length=100)
    buy3 = models.CharField(max_length=100)
    buy4 = models.CharField(max_length=100)
    buy5 = models.CharField(max_length=100)
    sell1 = models.CharField(max_length=100)
    sell2 = models.CharField(max_length=100)
    sell3 = models.CharField(max_length=100)
    sell4 = models.CharField(max_length=100)
    sell5 = models.CharField(max_length=100)
    average = models.CharField(max_length=100)