
from django.db import models


class Single(models.Model):
    single_id = models.AutoField()
    nec = models.BooleanField()
    title = models.CharField(max_length=128, default="题干")
    context_num = models.IntegerField()
    correct_id = models.IntegerField(default=0)
    context_1 = models.CharField(max_length=128, default="null")
    context_2 = models.CharField(max_length=128, default="null")
    context_3 = models.CharField(max_length=128, default="null")
    context_4 = models.CharField(max_length=128, default="null")
    context_5 = models.CharField(max_length=128, default="null")
    context_6 = models.CharField(max_length=128, default="null")
    context_7 = models.CharField(max_length=128, default="null")
    context_8 = models.CharField(max_length=128, default="null")


class Multi(models.Model):
    multi_id = models.AutoField()
    nec = models.BooleanField()
    title = models.CharField(max_length=128, default="题干")
    context_num = models.IntegerField()
    context_1 = models.CharField(max_length=128, default="null")
    context_2 = models.CharField(max_length=128, default="null")
    context_3 = models.CharField(max_length=128, default="null")
    context_4 = models.CharField(max_length=128, default="null")
    context_5 = models.CharField(max_length=128, default="null")
    context_6 = models.CharField(max_length=128, default="null")
    context_7 = models.CharField(max_length=128, default="null")
    context_8 = models.CharField(max_length=128, default="null")


class Pack(models.Model):
    pack_id = models.AutoField()
    nec = models.BooleanField()
    title = models.CharField(max_length=128, default="题干")
    pack_num = models.IntegerField()


class Rate(models.Model):
    rate_id = models.AutoField()
    nec = models.BooleanField()
    title = models.CharField(max_length=128, default="题干")
