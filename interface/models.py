from django.db import models
from django.contrib.auth.models import User
from monitoring.models import Asset
from django.utils import timezone


class AssetMonitoring(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    lower_limit = models.FloatField(default=None, null=True)
    upper_limit = models.FloatField(default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
