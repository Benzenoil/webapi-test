from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('message', 'user_id', 'nickname', 'comment')

class SignUpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('message', 'user_id', 'nickname', 'comment')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('a', 'b','c')