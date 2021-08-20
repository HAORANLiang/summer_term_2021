from django.db import models


# Create your models here.
class Single_ans(models.Model):
    single_id = models.AutoField(primary_key=True)
    ans = models.IntegerField()


class Multi_ans(models.Model):
    multi_id = models.AutoField(primary_key=True)
    num = models.IntegerField()
    ans1 = models.IntegerField(blank=True, null=True)
    ans2 = models.IntegerField(blank=True, null=True)
    ans3 = models.IntegerField(blank=True, null=True)
    ans4 = models.IntegerField(blank=True, null=True)
    ans5 = models.IntegerField(blank=True, null=True)
    ans6 = models.IntegerField(blank=True, null=True)
    ans7 = models.IntegerField(blank=True, null=True)
    ans8 = models.IntegerField(blank=True, null=True)


class Pack_ans(models.Model):
    pack_id = models.AutoField(primary_key=True)
    num = models.IntegerField()
    ans1 = models.CharField(max_length=255, blank=True, null=True)
    ans2 = models.CharField(max_length=255, blank=True, null=True)
    ans3 = models.CharField(max_length=255, blank=True, null=True)
    ans4 = models.CharField(max_length=255, blank=True, null=True)
    ans5 = models.CharField(max_length=255, blank=True, null=True)


class Rate_ans(models.Model):
    rate_id = models.AutoField(primary_key=True)
    ans = models.IntegerField()


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    list_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)


class Result_build(models.Model):
    result_build_id = models.AutoField(primary_key=True)
    list_id = models.IntegerField()
    que_no = models.IntegerField()
    que_type = models.CharField(max_length=255)
    que_id = models.IntegerField()
