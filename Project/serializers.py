from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *



class User_serializer(serializers.ModelSerializer):
      class Meta:
          fields = ["username",  "first_name",
                    "email", "date_joined", "password"]
          model = User
          

class Chat_serializer(serializers.ModelSerializer):
      class Meta:
            model = Chat
            
            fields = "__all__"
            

class Profile_serializer(serializers.ModelSerializer):
      class Meta:
            model = Profile
   
   
            fields = "__all__"
            
class Contact_serializer(serializers.ModelSerializer):
      class Meta:
            model = Contacts
            fields = "__all__"
            
            
class  Group_serializer(serializers.ModelSerializer):
      class Meta:
            model = Group
            fields = "__all__"
            
            

