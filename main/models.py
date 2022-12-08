from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=20)
    number = models.IntegerField()
    grades = models.IntegerField()
    pluses = models.IntegerField()
    class_name = models.CharField(max_length=2)
    visibility = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.second_name}'

class Code(models.Model):
    code = models.CharField(max_length=6)
    admin = models.BooleanField(default=False)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name