from django.urls import path,include
from .views import GetUserProfileView,UpdateUserProfile
urlpatterns=[
    path('user',GetUserProfileView.as_view()),
    path('update',UpdateUserProfile.as_view()),
    
]