from django.shortcuts import render
from .models import Employee
from rest_framework import viewsets
from .Serializers import employeeserializer
from .Serializers import departmentserializer
from .models import Department
from .models import Project,UserDetails,User
from .Serializers import Projectserializer,UserDetailsSerializer,UserSerializer,SignUpSerializer,LoginSerializer
from rest_framework import filters
from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
# Create your views here.
#employeeviewset---> class name
#viewsets.modelviewset---> DRF class that provides implementation for the crud operations
class employeeViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    #collection of objects from the databse using orm
    queryset = Employee.objects.all()
    serializer_class = employeeserializer
    #use the search filter funtionality
    #search filters is al built in feature provided by django
    filter_backends=[filters.SearchFilter]
    #specifies the fields in which the search should be performed
    search_fields=['employeename','designation']
    #http://127.0.0.1:8000/api/employees/?Search=abhijith


class departmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class=departmentserializer

class ProjectViewset(viewsets.ModelViewSet):
    queryset=Project.objects.all()
    serializer_class=Projectserializer

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset=UserDetails.objects.all()
    serializer_class=UserDetailsSerializer

#class based api- api view is provideed by djnago rest frame work
class SignupAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        Serializer=SignUpSerializer(data=request.data)
        if Serializer.is_valid():
            #if the validation success it will create a new user
            #DRF internally calls create method inside the serializer
            user=Serializer.save()
            #if toekn already exists , return the existing token otherwise it creates a new one
            # token,created=Token.objects.get_or_create(user=user)
            refresh=RefreshToken.for_user(user)
            return Response({
                "user_id":user.id,
                "username":user.username,
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                # 'token':token.key,
                "role":user.groups.all()[0].id if user.groups.exists() else None
            },status=status.HTTP_201_CREATED)
        else:
            res={'status':status.HTTP_400_BAD_REQUEST,'data':Serializer.errors}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes=[AllowAny]

    #run when POST/Login is called
    def post(self,request):
        #create a serializer object and it receives the username and password
        serializer=LoginSerializer(data=request.data)
        #serializer will validate the data
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=username,password=password)

            if user is not None:
                refresh=RefreshToken.for_user(user)
                # token=Token.objects.get(user=user)
                response={
                    "status":status.HTTP_200_OK, 
                    "message":"success",
                    "username":user.username,
                    "access":str(refresh.access_token),
                    "refresh":str(refresh),
                    # "token":token.key,
                    "role":user.groups.all()[0].id if user.groups.exists() else None

                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid Email or Password",

                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Bad Request",
                "data":serializer.errors
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


        