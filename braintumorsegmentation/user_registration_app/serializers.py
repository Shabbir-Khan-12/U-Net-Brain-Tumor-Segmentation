from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DumpSession
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

class GetGroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class GetUserSerializer(ModelSerializer):
    groups = GetGroupSerializer(many=True)

    class Meta:
        model = User
        exclude = ('password', 'user_permissions')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        group_names = instance.groups.values_list('name', flat=True)
        data['groups'] = group_names
        return data

class UserModelSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # exclude = ['pasword']
        
class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  # Serialize all fields of the Group model
        # Or specify specific fields you want to include: fields = ('name',)

class DumpSessionModelSerializers(ModelSerializer):
    class Meta:
        model = DumpSession
        fields = '__all__'

class PredictionImageSerializer(serializers.Serializer):
    image = serializers.ImageField()