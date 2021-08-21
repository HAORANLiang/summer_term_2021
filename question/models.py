
from django.db import models


class Single(models.Model):
    single_id = models.AutoField(primary_key=True)
    que_type = models.CharField(max_length=32)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
    content_num = models.IntegerField()
    correct_id = models.IntegerField()
    content_1 = models.CharField(max_length=128)
    content_2 = models.CharField(max_length=128)
    content_3 = models.CharField(max_length=128)
    content_4 = models.CharField(max_length=128)
    content_5 = models.CharField(max_length=128)
    content_6 = models.CharField(max_length=128)
    content_7 = models.CharField(max_length=128)
    content_8 = models.CharField(max_length=128)


class Multi(models.Model):
    multi_id = models.AutoField(primary_key=True)
    que_type = models.CharField(max_length=32)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
    content_num = models.IntegerField()
    content_1 = models.CharField(max_length=128)
    content_2 = models.CharField(max_length=128)
    content_3 = models.CharField(max_length=128)
    content_4 = models.CharField(max_length=128)
    content_5 = models.CharField(max_length=128)
    content_6 = models.CharField(max_length=128)
    content_7 = models.CharField(max_length=128)
    content_8 = models.CharField(max_length=128)


class Pack(models.Model):
    pack_id = models.AutoField(primary_key=True)
    que_type = models.CharField(max_length=32)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
    pack_num = models.IntegerField()


class Rate(models.Model):
    rate_id = models.AutoField(primary_key=True)
    que_type = models.CharField(max_length=32)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
