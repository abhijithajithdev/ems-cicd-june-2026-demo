from rest_framework import serializers
from .models import Department
from .models import Employee
from .models import Project,UserDetails
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password
from datetime import date
import re

#validation 1 : dateofjoining current date
#validation 2: employeename should be characters,no special characters
#validaion of dateofjoining
def dateofjoining_restriction(dateofjoining):
    today=date.today()
    if dateofjoining!=today:
        raise serializers.ValidationError("the date of joining must be today")
    return dateofjoining

#validation for employee name
def namevalidation(employee_name):
    if len(employee_name)<3 or not re.fullmatch(r"[A-Za-z]+(?: [A-Za-z]+)*", employee_name):
        raise serializers.ValidationError("Name must contain at least 3 characters; use letters separated by single spaces only.")
    return employee_name

# VALIDATION 3: Contact number
# Must contain exactly 10 digits
def contactvalidation(contact):
    if not re.match("^[0-9]{10}$", contact):
        raise serializers.ValidationError("Contact number must contain exactly 10 digits")
    return contact

# VALIDATION 4: Department name
def departmentnamevalidation(departmentname):
    if len(departmentname) < 2:
        raise serializers.ValidationError("Department name must contain at least 2 characters")
    return departmentname
        
#department serializer
class departmentserializer(serializers.ModelSerializer):
    departmentname=serializers.CharField(max_length=200,validators=[departmentnamevalidation])

    class Meta:
        model=Department
        fields='__all__'

#employee serilazer
class employeeserializer(serializers.ModelSerializer):
    department=departmentserializer(source='departmentid',read_only=True)
    dateofjoining=serializers.DateField()

    def validate_dateofjoining(self, value):
        # Keep existing employees editable while enforcing today for new employees.
        if self.instance is None:
            return dateofjoining_restriction(value)
        return value
    employeename=serializers.CharField(max_length=200,validators=[namevalidation])
    contact=serializers.CharField(validators=[contactvalidation])
    #show project_details
    project_details=serializers.StringRelatedField(source='projects',many=True,read_only=True)

    class Meta:
        model=Employee
        fields=('employeeid','employeename','designation','dateofjoining','contact',
                'isactive','departmentid','department','project_details')     

class Projectserializer(serializers.ModelSerializer):
    #employees--> get the data for the employee_details from the employees field of the project model
    employee_details=employeeserializer(source='employees',required=False,many=True,read_only=True)
    name=serializers.CharField(max_length=200,validators=[namevalidation])

    class Meta:
        model=Project
        fields=('id','name','employees','employee_details')

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserDetails
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=('id','username')


#receives the registeration data ,validates it and hashes the password createte user
# and assign th user to a group and finally returns the created user
class SignUpSerializer(serializers.ModelSerializer):
    group_name=serializers.CharField(write_only=True,required=False)

    def create(self,validated_data):
        group_name=validated_data.pop("group_name",None)

        #hash th epassword 
        validated_data["password"]=make_password(validated_data.get("password"))

        #create the user
        user=super(SignUpSerializer,self).create(validated_data)

        if group_name:
            group,created=Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user

    class Meta:
        model=User
        fields=['username','password','group_name']

class LoginSerializer(serializers.ModelSerializer):
    #field to get username from the user
    username=serializers.CharField()
    #field to get password from the user
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','password']
