from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import Group, User
from rest_framework.response import Response

from user_profile.models import UserProfile

from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
# from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.contrib import auth
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect,name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self,request,format=None):
        isAuthenticated=User.is_authenticated
        if isAuthenticated:
            return Response({'isAuthenticated':'success'})
        else:
            return Response({'isAuthenticated':'error'})

@method_decorator(csrf_protect,name='dispatch')
class SignupView(APIView):
    permission_classes=(permissions.AllowAny,)
    def post(self,request,format=None):
        data=self.request.data
        username=data['username']
        password=data['password']
        re_password=data['re_password']
        
        if password==re_password:
            try:
                if User.objects.filter(username=username).exists():
                    return Response({'error':'Username already exists'})
                else:
                    if len(password)<6:
                        return Response({'error':'Password must be at leat 6 characcters'})
                    else:
                        user=User.objects.create_user(username=username,password=password)
                        user.save()
                        user=User.objects.get(id=user.id)
                        user_profile=UserProfile(user=user,first_name='',last_name='',phone='',city='')
                        user_profile.save()
                        return Response({'success':'User created successfully'})
            except:
                return Response({"error":'Something went wrong when registering account'})
        else:
            return Response({'error':'Password do not match'})
        
@method_decorator(csrf_protect,name='dispatch')
class LoginView(APIView):
    permission_classes=(permissions.AllowAny,)
    def post(self,request,format=None):
        data=self.request.data
        username=data['username']
        password=data['password']
        try:
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return Response({'success':'User authenticated','username':username})
            else:
                return Response({'error':'Error Authentication'})
            
        except:
            return Response({'error':'Something went wrong when Loggin in'})
            
# @method_decorator
class LogoutView(APIView):
    def post(self,request,format=None):
        try:
            auth.logout(request)
            return Response({'success':'Logout Out'})
        except:
            return Response({'error':'Something went wrong when logging out'})
        
                
@method_decorator(ensure_csrf_cookie,name='dispatch')
class GetCSRFToken(APIView):
    
    permission_classes=(permissions.AllowAny,)
    def get(self,request,format=None):
        return Response({'success':'CSRF cookie set'})
class DeleteAccountView(APIView):
    def delete(self,request,format=None):
        user=self.request.user
        try:
            user=User.objects.filter(id=user.id).delete()
            return Response({'success':'User delete successfully'})
        except:
            return Response({'error':'Something went wrong when try to delete user'})
        
class GetUsersView(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self,request,format=None):
        users=User.objects.all()
        
        users=UserSerializer(users,many=True)
        return Response(users.data)