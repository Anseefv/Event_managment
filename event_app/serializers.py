from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=CustomUser
        fields=['username','password','email','phone','role']

    password=serializers.CharField(write_only=True)


    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    

class PendingSerializer(serializers.ModelSerializer):

    employee=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=PendingList
        fields='__all__'
        read_only_fields=['employee',"status"]


class EmployeeProfileSerializer(serializers.ModelSerializer):

    name=serializers.SerializerMethodField()

    class Meta:
            model=Profile
            fields='__all__'
            read_only_fields=['wage','over_time_wage','id','owner']

    def get_name(self,obj):
         return obj.owner.username

    

class SupervisorProfileSerializer(serializers.ModelSerializer):

    name=serializers.SerializerMethodField()

    class Meta:
            model=Profile
            fields='__all__'
            read_only_fields=['photo','age','id','owner']

    def get_name(self,obj):
             return obj.owner.username

