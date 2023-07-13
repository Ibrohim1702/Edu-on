from django.db import models


class Log(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False)
    messages = models.JSONField(default={"state": 0})

    def __str__(self):
        return "#%s" % self.user_id


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False)
    user_name = models.CharField(max_length=256, null=True)
    first_name = models.CharField(max_length=256, null=True)
    menu = models.IntegerField(null=True)
    # subscribe = models.BooleanField(default=False)
    # kurs = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.user_id} {self.first_name}"


class Category(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128)
    ctg = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Sub(models.Model):
    name = models.CharField(max_length=256)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Videos(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    video = models.IntegerField()
    chat_id = models.BigIntegerField(default=5392556467)

    def __str__(self):
        return self.sub.name
