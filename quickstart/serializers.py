from rest_framework import serializers
from .models import Snippet, Signup


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = ('user_id', 'nickname', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = ('user_id', 'nickname', 'comment')


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
