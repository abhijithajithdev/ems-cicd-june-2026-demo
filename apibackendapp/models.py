from django.db import models
from django.contrib.auth.models import User

#A model is a python class that represents a table in a database
# Create your models here.

class Department(models.Model):
    departmentID=models.AutoField(primary_key=True)
    departmentname=models.CharField(max_length=100)

    def __str__(self):
        return self.departmentname

    
class Employee(models.Model):
    employeeid=models.AutoField(primary_key=True)
    employeename=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    dateofjoining=models.DateField()
    departmentid=models.ForeignKey(Department,on_delete=models.CASCADE)
    contact=models.CharField(max_length=15)
    isactive=models.BooleanField(default=True)

    def __str__(self):
        return self.employeename


class Project(models.Model):
    #for a many to many relationship model we cannot explicity define an id field 
    #django will br efereing to the deafult id field ld
    name=models.CharField(max_length=100,unique=True)
    #defineing a mapny-to-many field
    #realted name of this relation will be later reffered in the serializer
    employees=models.ManyToManyField(Employee,related_name='Projects')

    def __str__(self):
        return self.name


class UserDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_details')
    phoneno=models.CharField(max_length=15)
    email=models.EmailField()

    def __str__(self):
        return self.user.username
