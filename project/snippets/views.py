from __future__ import unicode_literals
from rest_framework import status
from snippets.models import  User , Project
from snippets.models import  User , Project, UserLog
from rest_framework.generics import CreateAPIView , RetrieveAPIView, ListAPIView ,ListCreateAPIView
from snippets.serializers import  UserFetchSerializer, UserCreateSerializer, UserLoginSerializer, ProjectSerializer, UserLogDataSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate, login, logout
from rest_framework import authentication , permissions , status
from snippets.permissions import IsAdmin , IsClient
from rest_framework.decorators import permission_classes , authentication_classes
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from snippets.forms import LoginForm
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
import json
import traceback
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

def hello(request):
    token = request.COOKIES.get('auth')
    print token
    request.COOKIES['auth'] = ""
    print token
    # user = Token.objects.filter(auth_token=str(token))
    # print token.user
    return render(request, "home.html")

def employee(request):
   return render(request, "employee.html")

def admin(request):
    print "tempdsdsdsdsds"
    return render(request, "admin.html")

class CreateProject(APIView):
    def get(self, request, format=None):
        return render(request, "createProject.html")

class EditProject(APIView):
    def get(self, request, format=None):
        return render(request, "editproject.html")

class CreateUser(APIView):
    def get(self, request, format=None):
        return render(request, "createUser.html")

class DeleteUser(APIView):
    def get(self, request, format=None):
        return render(request, "hello4.html")

def Client(request):
   return render(request, "client.html")

#----------------------------------------------------UserLogin/LogoutAPIs---------------------------------------------#
class LoginAPIView(APIView):
    def post(self, request):
        try:
            serializer_class = UserLoginSerializer
            data = request.POST
            print request.is_ajax()
            print data
            if len(data) > 2 :
                print 'extra arguments sent'
                return Response({"extra parameters sent"}, status.HTTP_409_CONFLICT)
            usern = data.get('username', '')
            passw = data.get('password','')
            if ( not usern ) or ( not passw ):
                return Response({"username or password not sent from client side"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            user = authenticate(username = usern, password = passw)
            if user is not None:
                 login(request, user)
            if not user :
                return Response({"no such user exists"},status.HTTP_204_NO_CONTENT)
            token_key = user.get_or_create_auth_token()
            details = UserFetchSerializer(user).data
            details['auth_token']= token_key
            temp = UserLogDataSerializer(data={'Name' : user.username , 'Action' : 'Login'})
            if temp.is_valid():
                print "isvalid"
                temp.save()
            print request.user
            response = Response(details, status.HTTP_200_OK)
            response.set_cookie('auth', request.user.get_or_create_auth_token())
            return response
        except Exception as e :
            return Response({'error': str(e)}, status=500)

class Logout(APIView):
    def get(self, request):
        try :
            print request.user
            token = request.COOKIES.get('auth')
            print token
            if ( request.user.is_anonymous() ):
                return Response({"Valid Auth Token not sent from client side"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            print request.user
            temp = UserLogDataSerializer(data={'Name': request.user.username, 'Action': 'LogOut'})
            if temp.is_valid():
                temp.save()
            details = {}
            response = Response(details, status.HTTP_200_OK)
            response.delete_cookie('auth')
            request.user.auth_token.delete()
            logout(request)
            return Response(details,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'error': str(e)}, status=500)

#--------------------------------------BackEnd API's-----------------------------------------------------------------#

class UserList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

    # to fetch userllist of a type , type must be sent as a url parameter , only for admin
    def get(self, request):
        try:
            u_type = request.GET.get('user_type','')
            users = User.objects.filter(UserType=str(u_type))
            print u_type
            print users
            serializer = UserFetchSerializer(users, many=True)
            return Response([serializer.data], status.HTTP_200_OK)
        except Exception as e:
            return Response({"No users data is in database"}, status.HTTP_204_NO_CONTENT)

class ProjectList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

    def get(self, request, format=None):
        try:
            projects = Project.objects.filter()
            serializer = ProjectSerializer(projects, many=True)
            if len(serializer.data) == 0:
                return Response([serializer.data],status.HTTP_204_NO_CONTENT)
            print serializer.data
            return Response( [serializer.data] ,status.HTTP_200_OK )
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GetCount(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

    def get(self, request, format=None):
        try:
            projects = Project.objects.all()
            clients = User.objects.filter(UserType='C')
            employees = User.objects.filter(UserType='E')
            admins= User.objects.filter(UserType='A')

            serializer = ProjectSerializer(projects, many=True)
            noOfProjects = len(serializer.data)
            print noOfProjects

            serializer = UserFetchSerializer(clients, many=True)
            noOfClients = len(serializer.data)
            print noOfClients

            serializer = UserFetchSerializer(employees, many=True)
            noOfEmployees = len(serializer.data)
            print noOfEmployees

            serializer = UserFetchSerializer(admins, many=True)
            noOfAdmins = len(serializer.data)
            print noOfAdmins

            return Response( {"pCount":noOfProjects,"eCount":noOfEmployees,"cCount":noOfClients,"aCount":noOfAdmins} ,status.HTTP_200_OK )
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class UserLogList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

    def get(self, request, format=None):
        try:
            userlogs = UserLog.objects.all()
            serializer = UserLogDataSerializer(userlogs, many=True)
            if len(serializer.data) == 0:
                return Response([serializer.data],status.HTTP_204_NO_CONTENT)
            print serializer.data
            return Response( [serializer.data] ,status.HTTP_200_OK )
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class UserInstance(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

    # to fetch a  user , id must be sent as a url parameter , only for admin
    def get(self, request, format=None):
        try:
            u_type = request.user.UserType
            print u_type
            if (u_type != 'A'):
                return Response({"Sorry , you are not authorised for this operation"}, status.HTTP_200_OK)
            UserId = request.GET.get('Id','')
            print "yes"
            print UserId
            print "No"
            if not UserId:
                return Response({"id not sent from client side"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            user = User.objects.get(Id=UserId)
            if not user:
                return Response({"Client does not exist"}, status=status.HTTP_204_NO_CONTENT)
            serializer = UserFetchSerializer(user)
            return Response([serializer.data], status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    # to create a new user , fields must be sent as body parameters , only for admin
    def post(self, request):
        try :
            u_type = request.user.UserType
            print u_type
            if (u_type != 'A'):
                return Response({"Sorry , you are not authorised for this operation"}, status.HTTP_200_OK)
            request_data = request.POST
            serializer = UserCreateSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                u = User.objects.get(username=serializer.data['username'])
                u.set_password(request_data['password'])
                u.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def put(self, request, format=None):
        UserId = request.GET.get('Id', '')
        user = User.objects.get(Id=UserId)
        print "temp"
        print user
        serializer = UserCreateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            u = User.objects.get(username=serializer.data['username'])
            u.set_password(request.data['password'])
            u.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request , format=None):
        try :
            u_type = request.user.UserType
            print u_type
            print "yes"
            if (u_type != 'A'):
                return Response({"Sorry , you are not authorised for this operation"}, status.HTTP_200_OK)
            clientId = request.GET.get('Id','')
            print "no"
            print clientId
            print "yes"
            if not clientId:
                return Response({"id not sent from client side"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            Client = User.objects.get(Id = clientId)
            print Client
            Client.delete()
            return Response({"Deleted"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e :
            return Response({'error': str(e)}, status=500)

class SetProjectStatus(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    #to set project status , only admin
    def post(self, request ):
        try:
            projectId = request.GET.get('id', '')
            status = request.GET.get('status', '')
            project = Project.objects.filter(id=projectId)

            if ( status == 'Pending' ):
                project.isPending = 1
                print (project.isPending)

            if ( status == 'Delievered'):
                project.isDeliever = 1
                print project.isDeliever
            return Response( {'status set'}  )
        except Exception as e :
            return Response({'error': str(e)}, status=500)

class ProjectInstance(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    # to fetch/read a project instance by id, only admin
    def get(self, request, format=None):
        try:
            projectId = request.GET.get('Id','')
            print "temp"
            print projectId
            if not projectId:
                return Response({}, status.HTTP_200_OK)
            project = Project.objects.filter(Id=projectId)
            print "temp"
            print project[0]
            serializer = ProjectSerializer(project[0])
            return Response([serializer.data],status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def post(self, request, format=None):
        print "temp"
        try:
            u_type = request.user.UserType
            print u_type
            request_data = request.POST
            print "temp again"
            if (u_type != 'A'):
                return Response({"Sorry , you are not authorised for this operation"}, status.HTTP_200_OK)
            serializer = ProjectSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print serializer.errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def put(self, request, format=None):
        try:
            projectId = request.GET.get('Id', '')
            project = Project.objects.get(Id=projectId)
            serializer = ProjectSerializer(project,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def delete(self, request, format=None):
        try:
            print "temp"
            projectId = request.GET.get('Id', '')
            project = Project.objects.filter(Id=projectId)
            project.delete()
            return Response({"Deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

#1------------------------Using Generic APIs---------------------------#

# class ProjectlistAPIView(ListAPIView):
#     serializer_class = ProjectSerializer
#
#     def get_queryset(self):
#         return Project.objects.all()
#
# class ProjectlistCreateAPIView(ListCreateAPIView):
#     serializer_class = ProjectSerializer
#
#     def get_queryset(self):
#         return Project.objects.all()
#
# class ClientlistAPIView(ListAPIView):
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         return User.objects.filter(user_type = 'C')
#
# class ClientlistCreateAPIView(ListCreateAPIView):
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         return User.objects.filter(user_type = 'C')
#
# class AdminlistAPIView(ListAPIView):
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         return User.objects.filter(user_type = 'A')
#
# class AdminlistCreateAPIView(ListCreateAPIView):
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         return User.objects.filter(user_type = 'A')


