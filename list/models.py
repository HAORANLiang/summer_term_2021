
from django.db import models


class List(models.Model):
    list_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=64)
    list_type = models.CharField(max_length=32)
    list_name = models.CharField(max_length=128)
    full_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    last_edit_time = models.DateTimeField()
    owner_id = models.IntegerField()
    que_num = models.IntegerField()
    summary = models.CharField(max_length=256)
    list_num = models.IntegerField()


class Que_build(models.Model):
    que_build_id = models.AutoField(primary_key=True)
    list_id = models.IntegerField()
    que_no = models.IntegerField()
    que_type = models.CharField(max_length=16)
    que_id = models.IntegerField()
