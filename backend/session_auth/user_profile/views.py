

# Create your views here.

from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import  User
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
class GetUserProfileView(APIView):
    def get(self,request,format=None):
        try:
            user=self.request.user
            username=user.username
            user=User.objects.get(id=user.id)
        # username=user.username
            user_profile=UserProfile.objects.get(user=user)
            user_profile=UserProfileSerializer(user_profile)
            return Response({'profile':user_profile.data,'username':str(username)})
        except:
            return Response ({'error':'Something went wrong when retrieving profile'})
        
class UpdateUserProfile(APIView):
    def put(self,request,format=None):
        try:
            user=self.request.user
            username=user.username
            data=self.request.data
        
            first_name=data['first_name']
            last_name=data['last_name']
            phone=data['phone']
            city=data['city']
            user_profile = UserProfile.objects.get(user=user)

            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.phone = phone
            user_profile.city = city
            user_profile.save()

            user_profile = UserProfileSerializer(user_profile)
            return Response({'profile': user_profile.data, 'username': str(username)})
        except:
            return Response({'error':'Something went wrong when updating profile'})
            
        