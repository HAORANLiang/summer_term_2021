
from django.db import models


class Single(models.Model):
    single_id = models.AutoField(primary_key=True)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
    context_num = models.IntegerField()
    correct_id = models.IntegerField()
    context_1 = models.CharField(max_length=128)
    context_2 = models.CharField(max_length=128)
    context_3 = models.CharField(max_length=128)
    context_4 = models.CharField(max_length=128)
    context_5 = models.CharField(max_length=128)
    context_6 = models.CharField(max_length=128)
    context_7 = models.CharField(max_length=128)
    context_8 = models.CharField(max_length=128)


class Multi(models.Model):
    multi_id = models.AutoField(primary_key=True)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
    context_num = models.IntegerField()
    context_1 = models.CharField(max_length=128)
    context_2 = models.CharField(max_length=128)
    context_3 = models.CharField(max_length=128)
    context_4 = models.CharField(max_length=128)
    context_5 = models.CharField(max_length=128)
    context_6 = models.CharField(max_length=128)
    context_7 = models.CharField(max_length=128)
    context_8 = models.CharField(max_length=128)


class Pack(models.Model):
    pack_id = models.AutoField(primary_key=True)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
    pack_num = models.IntegerField()


class Rate(models.Model):
    rate_id = models.AutoField(primary_key=True)
    nec = models.BooleanField()
    title = models.CharField(max_length=128)
