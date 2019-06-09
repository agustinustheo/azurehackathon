from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Review(models.Model):
    yt_id = models.CharField(max_length=20, default="")
    title = models.CharField(max_length=150, default="")
    anger_count = models.IntegerField(default=0)
    tense_count = models.IntegerField(default=0)
    micro_anger_count = models.IntegerField(default=0)
    micro_tense_count = models.IntegerField(default=0)
    anger_timestamp = JSONField(blank=True, null=True)
    tense_timestamp = JSONField(blank=True, null=True)
    micro_anger_timestamp = JSONField(blank=True, null=True)
    micro_tense_timestamp = JSONField(blank=True, null=True)
    finish_processing = models.BooleanField()
    error = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.yt_id