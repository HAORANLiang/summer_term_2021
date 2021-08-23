from django.db import models


class List(models.Model):
    list_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=64)
    list_type = models.CharField(max_length=32)
    list_name = models.CharField(max_length=128)
    full_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    publish_time = models.DateTimeField(null=True)
    last_edit_time = models.DateTimeField(auto_now=True, null=True)
    owner_id = models.IntegerField()
    que_num = models.IntegerField()
    summary = models.CharField(max_length=256)
    only_once = models.BooleanField(default=True)
    need_login = models.BooleanField(default=True)
    list_num = models.IntegerField()


class Que_build(models.Model):
    que_build_id = models.AutoField(primary_key=True)
    list_id = models.IntegerField()
    que_no = models.IntegerField()
    que_type = models.CharField(max_length=16)
    que_id = models.IntegerField()
