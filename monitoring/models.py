from django.db import models
from django.utils import timezone


class Asset(models.Model):
    code = models.CharField(max_length=10, db_index=True, unique=True)
    name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=100, null=True)
    document = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=30)
    market_time_open = models.TimeField()
    market_time_close = models.TimeField()
    market_time_timezone = models.IntegerField()
    market_cap = models.FloatField(null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class AssetPrice(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.FloatField()
    change_percent = models.FloatField()
    currency = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
