from django.db import models
import os
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    face_encoding = models.BinaryField()  # Store face encoding as binary data
    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} Present Marked on {self.date} at {self.time}"

class New_Commers_Validate(models.Model):
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10,unique=True)

    class Meta:
        unique_together = ('f_name', 'l_name')

    def __str__(self):
        return f"{self.f_name} {self.l_name}"

class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField()
    phone =models.IntegerField()
    desc = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.name