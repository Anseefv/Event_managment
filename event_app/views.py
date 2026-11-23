from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import*
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class RegisterView(CreateAPIView):

    authentication_classes=[TokenAuthentication]
    serializer_class=RegisterSerializer
    queryset=CustomUser.objects.all()
    permission_classes=[IsAuthenticated,RegisterPermission]


    def perform_create(self, serializer):


        if self.request.user.role =='admin':
            data=self.request.data.get('role')
            if not data:
                return serializer.save(role='employee')

        if self.request.user.role =='supervisor':
            data=self.request.data.get('role')
            if data:
                raise ValidationError('you cannot assign role')
            return serializer.save(role='employee')
        return serializer.save()



class PendingListView(ModelViewSet):

    authentication_classes=[TokenAuthentication]
    serializer_class=PendingSerializer
    permission_classes=[IsAuthenticated,PendingListPermission]

    def get_queryset(self):

        if self.request.user.role=='employee':
            return PendingList.objects.filter(employee=self.request.user)

        return PendingList.objects.filter(status='pending')

    def perform_create(self, serializer):
        return serializer.save(employee=self.request.user)
    def perform_update(self, serializer):
        return serializer.save(status='pending')



class DecidingApiView(CreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DecisionPermission]
    def get_queryset(self):
        return PendingList.objects.filter(status='pending')

    def create(self, request, *args, **kwargs):

        decision = self.kwargs.get('decision')
        if decision not in ['accept','reject']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = get_object_or_404(self.get_queryset(),id=kwargs.get('pk'))
        if decision == "accept":
            return Response({"status": "ok perfect"})
        else :
            data.status='rejected'
            data.save()
            return Response(
                {"message": "Request rejected"},
                status=status.HTTP_200_OK
            )



class ProfileViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ProfilePermissions]

    def get_serializer_class(self):

        if self.request.user.role in ['admin','supervisor']:
            return SupervisorProfileSerializer

        return EmployeeProfileSerializer

    def get_queryset(self):

        if self.request.user.role in ['admin','supervisor']:
            return Profile.objects.filter(owner__role="employee")
        
        

        return Profile.objects.filter(owner=self.request.user)


    def perform_create(self, serializer):

        if Profile.objects.filter(owner=self.request.user).exists():
            raise serializers.ValidationError("Profile already exists")
        return serializer.save(owner=self.request.user)

